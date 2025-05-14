# 🛍️ ShopBot – E-Commerce AI Assistant with OpenAI Assistants API

**ShopBot** is a conversational AI assistant built with Python and OpenAI's `Assistants API` (using `gpt-4o`) to simulate a smart product advisor for an e-commerce platform. It supports dynamic function calling to retrieve product details and stock information from a mock catalog.

---

## 📌 Features

- Conversational AI assistant powered by OpenAI `gpt-4o`
- Dynamic function calling (`getProductInfo`, `checkStock`)
- In-memory product catalog with at least 5 sample products
- Simulated conversation via command-line interface (CLI)
- Clean modular design with reusable components

---

## 🧠 Use Case Example

```text
You: Tell me about the Organic Cotton T-Shirt  
ShopBot: The Organic Cotton T-Shirt is a soft, breathable, and sustainable T-shirt. It costs $22.50.  

You: Is it available?  
ShopBot: Yes, the Organic Cotton T-Shirt is currently in stock (5 available).

