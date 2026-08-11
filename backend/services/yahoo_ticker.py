from __future__ import annotations

from typing import Any, Dict, Optional

from backend.stock_universe import STOCK_UNIVERSE


# ============================================================
# GHANIYAA YAHOO TICKER RESOLVER
# ============================================================
#
# IMPORTANT:
#
# Never blindly do:
#
#     symbol + ".NS"
#
# because STOCK_UNIVERSE is keyed by master identity.
#
# Example master key:
#
#     ISIN:INE294B01019
#
# Its actual record may contain:
#
#     symbol: "ABC"
#     nse_yahoo_symbol: "ABC.NS"
#     bse_yahoo_symbol: "123456.BO"
#
# This resolver always uses the master record first.
#
# ============================================================


def normalize_input(value: Any) -> str:
    """
    Normalize a user/application stock identifier.

    Examples:

        TCS
        tcs
        TCS.NS
        TCS.BO
        ISIN:INE467B01029
    """

    if value is None:
        return ""

    return str(value).strip().upper()


def _clean_ticker(value: Any) -> str:
    """
    Clean a Yahoo ticker without inventing a suffix.
    """

    if value is None:
        return ""

    value = str(value).strip().upper()

    if not value:
        return ""

    return value


def _record_symbol(record: Dict[str, Any]) -> str:
    """
    Return the canonical exchange symbol stored in the master record.
    """

    symbol = record.get("symbol")

    if not symbol:
        return ""

    return str(symbol).strip().upper()


def _record_isin(record: Dict[str, Any]) -> str:
    """
    Return normalized ISIN.
    """

    isin = record.get("isin")

    if not isin:
        return ""

    return str(isin).strip().upper()


def _build_indexes():
    """
    Build lookup indexes from STOCK_UNIVERSE.

    The master file is keyed by identity, not necessarily symbol.

    Example:

        ISIN:INE467B01029 -> TCS

    Therefore we cannot assume:

        STOCK_UNIVERSE["TCS"]

    exists.
    """

    by_symbol: Dict[str, Dict[str, Any]] = {}
    by_isin: Dict[str, Dict[str, Any]] = {}

    for key, record in STOCK_UNIVERSE.items():

        if not isinstance(record, dict):
            continue

        symbol = _record_symbol(record)

        if symbol:
            by_symbol[symbol] = record

        isin = _record_isin(record)

        if isin:
            by_isin[isin] = record

        # Also index the actual master key.
        normalized_key = normalize_input(key)

        if normalized_key.startswith("ISIN:"):

            key_isin = normalized_key[5:].strip()

            if key_isin:
                by_isin[key_isin] = record

    return by_symbol, by_isin


# Build once when module loads.
_BY_SYMBOL, _BY_ISIN = _build_indexes()


def refresh_yahoo_ticker_indexes() -> None:
    """
    Rebuild resolver indexes.

    Call this after STOCK_UNIVERSE is modified/reloaded.
    """

    global _BY_SYMBOL
    global _BY_ISIN

    _BY_SYMBOL, _BY_ISIN = _build_indexes()


def get_master_record(identifier: Any) -> Optional[Dict[str, Any]]:
    """
    Resolve an identifier to its master record.

    Supported:

        TCS
        TCS.NS
        TCS.BO
        ISIN:INE467B01029
    """

    value = normalize_input(identifier)

    if not value:
        return None

    # --------------------------------------------------------
    # Direct master key lookup
    # --------------------------------------------------------

    direct = STOCK_UNIVERSE.get(value)

    if isinstance(direct, dict):
        return direct

    # --------------------------------------------------------
    # ISIN lookup
    # --------------------------------------------------------

    if value.startswith("ISIN:"):

        isin = value[5:].strip()

        if isin:
            return _BY_ISIN.get(isin)

        return None

    # --------------------------------------------------------
    # Remove Yahoo suffix
    # --------------------------------------------------------

    base = value

    if base.endswith(".NS"):
        base = base[:-3]

    elif base.endswith(".BO"):
        base = base[:-3]

    # --------------------------------------------------------
    # Symbol lookup
    # --------------------------------------------------------

    return _BY_SYMBOL.get(base)


def get_yahoo_ticker(
    identifier: Any,
    exchange: Optional[str] = None,
) -> Optional[str]:
    """
    Resolve an application/master identifier to a Yahoo Finance ticker.

    Parameters
    ----------
    identifier:
        TCS
        TCS.NS
        TCS.BO
        ISIN:INE467B01029

    exchange:
        Optional:

            NSE
            BSE

        If omitted, NSE is preferred when available.

    Returns
    -------
    str | None

        Example:

            TCS.NS
            TCS.BO

    """

    value = normalize_input(identifier)

    if not value:
        return None

    requested_exchange = (
        str(exchange).strip().upper()
        if exchange
        else None
    )

    # --------------------------------------------------------
    # Already a real Yahoo ticker
    # --------------------------------------------------------

    if value.endswith(".NS"):
        base = value[:-3]

        record = _BY_SYMBOL.get(base)

        if record:

            nse_ticker = _clean_ticker(
                record.get("nse_yahoo_symbol")
            )

            if nse_ticker:
                return nse_ticker

        return value

    if value.endswith(".BO"):
        base = value[:-3]

        record = _BY_SYMBOL.get(base)

        if record:

            bse_ticker = _clean_ticker(
                record.get("bse_yahoo_symbol")
            )

            if bse_ticker:
                return bse_ticker

        return value

    # --------------------------------------------------------
    # Resolve master record
    # --------------------------------------------------------

    record = get_master_record(value)

    if not record:

        return None

    # --------------------------------------------------------
    # Explicit NSE request
    # --------------------------------------------------------

    if requested_exchange == "NSE":

        ticker = _clean_ticker(
            record.get("nse_yahoo_symbol")
        )

        if ticker:
            return ticker

        return None

    # --------------------------------------------------------
    # Explicit BSE request
    # --------------------------------------------------------

    if requested_exchange == "BSE":

        ticker = _clean_ticker(
            record.get("bse_yahoo_symbol")
        )

        if ticker:
            return ticker

        return None

    # --------------------------------------------------------
    # Default:
    #
    # Prefer NSE.
    # --------------------------------------------------------

    nse_ticker = _clean_ticker(
        record.get("nse_yahoo_symbol")
    )

    if nse_ticker:
        return nse_ticker

    # --------------------------------------------------------
    # Otherwise use BSE.
    # --------------------------------------------------------

    bse_ticker = _clean_ticker(
        record.get("bse_yahoo_symbol")
    )

    if bse_ticker:
        return bse_ticker

    # --------------------------------------------------------
    # Last-resort compatibility:
    #
    # Only use a normal symbol.
    #
    # NEVER append .NS to an ISIN key.
    # --------------------------------------------------------

    symbol = _record_symbol(record)

    if symbol and not symbol.startswith("ISIN:"):

        return f"{symbol}.NS"

    return None


def get_yahoo_symbol(
    identifier: Any,
    exchange: Optional[str] = None,
) -> Optional[str]:
    """
    Alias for get_yahoo_ticker().
    """

    return get_yahoo_ticker(
        identifier,
        exchange=exchange,
    )


def is_resolvable_yahoo_ticker(
    identifier: Any,
    exchange: Optional[str] = None,
) -> bool:
    """
    Return True when the identifier resolves to a Yahoo ticker.
    """

    return bool(
        get_yahoo_ticker(
            identifier,
            exchange=exchange,
        )
    )


def get_yahoo_ticker_info(
    identifier: Any,
) -> Dict[str, Any]:
    """
    Diagnostic helper.

    Returns the original identifier, master identity,
    symbol, ISIN and available Yahoo tickers.
    """

    record = get_master_record(identifier)

    if not record:

        return {
            "identifier": normalize_input(identifier),
            "found": False,
            "yahoo_ticker": None,
        }

    return {
        "identifier": normalize_input(identifier),
        "found": True,
        "symbol": record.get("symbol"),
        "isin": record.get("isin"),
        "nse_yahoo_symbol": record.get(
            "nse_yahoo_symbol"
        ),
        "bse_yahoo_symbol": record.get(
            "bse_yahoo_symbol"
        ),
        "default_yahoo_ticker": get_yahoo_ticker(
            identifier
        ),
        "nse_ticker": get_yahoo_ticker(
            identifier,
            exchange="NSE",
        ),
        "bse_ticker": get_yahoo_ticker(
            identifier,
            exchange="BSE",
        ),
    }