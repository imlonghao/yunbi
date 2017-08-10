# yunbi
A Python wrapper for the yunbi.com api

![PyPI](https://img.shields.io/pypi/v/yunbi.svg?style=flat-square) ![license](https://img.shields.io/github/license/imlonghao/yunbi.svg?style=flat-square)

## Install

You can install and upgrade this wrapper from pip:

```
$ pip install -U yunbi
```

## Docs

This wrapper is based on the API list on yunbi.com, you can check it out from [YUNBI EXCHANGE API LIST](https://yunbi.com/swagger/#/default).

What you need to know is that,

in `get_trades` and `get_trades_my` functions, the official API use `from` as a key, which is also a reserved words in Python.

To solve this problem, you need to use `from_id` instead of `from`.

For example,

```
get_trades('ethcny', from_id=123456)
```

## Example

```
from yunbi import Yunbi

y = Yunbi() # Access to public API
y.get_tickers_market('ethcny') # Get ETH/CNY market's tickets

y = Yunbi('YOUR API KEY', 'YOUR SECRET KEY') # Access to public and private API
y.get_members_me() # Get your account information
```

## License

[MIT License](https://github.com/imlonghao/yunbi/blob/master/LICENSE)
