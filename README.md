# Assignment Project: Real-Time Paper Trading and Backtesting Platform

This project is an advanced platform where users can design, test, and simulate simple trading strategies. It features a strategy builder for defining rules, connects to a brokerage API for market data, and includes a backtesting engine to run strategies against historical data. The platform also offers a real-time paper trading dashboard that uses WebSockets to display live portfolio updates as the market moves.


---

## Data Model

The data model is designed around three core entities: **Strategies**, **Rules**, and **Trades**. A `Strategy` is the central object, which contains one or more `Rules` that define its logic. When a strategy is simulated, it generates `Trades`, which are historical records of its performance.

Key relationships include:
*   A one-to-many relationship from `Strategy` to `Rule` (`on_delete=CASCADE`).
*   A one-to-many relationship from `Strategy` to `Trade` (`on_delete=PROTECT`) to preserve trade history.

![ER Diagram](docs/notes/er_diagram.png)


## Views and Templates

For this assignment, the full Django request-response cycle was implemented to display data from the models. Two separate function-based views were created to demonstrate different methods of rendering a template: one using a manual `HttpResponse` and another using the `render()` shortcut. Both views serve the same template, which dynamically displays a list of trades from the database and includes a fallback message for when no trades are present.

## Class-Based Views (CBVs) & URL Refactoring
For this assignment, two styles of Class-Based Views (CBVs) were implemented: a base view inheriting from `django.views.View` and a generic view using `ListView`. This demonstrates the evolution from manual method handling to leveraging Django's powerful generic views. The project's URL structure was also refactored to use `include()`, making the app more modular and maintainable.

## Filtering and Aggregation
The Strategy list page now includes a search feature to filter strategies by name. The page also computes and displays summary statistics, such as the total number of strategies and grouped counts of rules and trades per strategy, using the Django ORM's `aggregate()` and `annotate()` functions.