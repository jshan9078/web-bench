# 17-currency-meal-budget

- **kind**: read + arithmetic, cross-site (LLM-judge)
- **site**: xe.com + numbeo.com
- **what it tests**: cross-site data gathering with a computation joining the two
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: both live figures match their captured pages and the division is correct.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
First, on XE (https://www.xe.com), convert 2,500 CAD to Japanese yen at the current mid-market rate
and report the rate and the converted amount. Then, on Numbeo (https://www.numbeo.com), find the
current average price of an inexpensive restaurant meal in Tokyo, in yen. Finally compute how many
such meals the converted amount buys (round down). End with the rate, the JPY amount, the meal
price, and the meal count.
```
