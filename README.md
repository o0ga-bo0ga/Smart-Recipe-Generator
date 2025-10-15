# Smart Recipe Generator 🥣

A web application that uses LLM (Large Language Models) and image services to generate recipes from user‑provided ingredients, parse recipes, store them in a database, and generate images.  

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Architecture & Modules](#architecture--modules)  
4. [Approach & Methodology](#approach--methodology)  
   - [Recipe Generation (LLM)](#recipe-generation-llm)  
   - [Recipe Parsing](#recipe-parsing)  
   - [Image Generation / Image Service](#image-generation--image-service)  
   - [Database & Persistence](#database--persistence)  
   - [Workflow / Data Flow](#workflow--data-flow)  
5. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Configuration / Environment Variables](#configuration--environment-variables)  
   - [Running the App](#running-the-app)  
6. [Usage](#usage)  
7. [Project Structure](#project-structure)  

---

## Overview

Smart Recipe Generator is a tool that lets users input a set of ingredients or preferences and then:

- Generates a recipe (ingredients + instructions) using a language model  
- Parses generated recipe text into structured form  
- Optionally generates an image of the dish  
- Saves recipes into a database for later retrieval  

It is designed to combine AI generation and structured processing in a pipeline to give a usable recipe output.

---

## Features

- Prompt-based recipe generation  
- Parsing of recipe text into structured data (steps, ingredients, quantities)  
- Generation or retrieval of dish images (via an image service)  
- Storage of recipes in a database  
- UI integration (front end to call backend services)  
- Modular services (LLM service, image service, parser, DB service)  

---

## Architecture & Modules

| Module / File | Responsibility |
|---|---|
| `app.py` | Main Flask (or FastAPI / web) application entry point, routes and orchestration |
| `llm_service.py` | Interacts with LLM / OpenAI API to generate recipe text from prompts |
| `recipe_parser.py` | Parses the raw recipe text (ingredients, steps) into structured representation |
| `image_service.py` | Generates or fetches an image for the dish (e.g. via a diffusion model API) |
| `db_service.py` | Handles database operations: insert, fetch recipes, etc. |
| `data/` | Any static data or seed data used by the application |
| `results/` | Possibly output / generated files (images, JSON outputs) |
| `templates/`, `static/` | Front-end templates, CSS if web UI exists |
| `recipes.db` | SQLite (or whichever) database file used locally |
| `requirements.txt` | Python dependencies |

---

## Approach & Methodology

### Recipe Generation (LLM)
1. User inputs ingredients and preferences.  
2. A structured prompt is built and sent to the LLM.  
3. The model returns raw recipe text.  
4. The response is passed for parsing.

### Recipe Parsing
- Converts text to structured data (JSON or dict) using regex/heuristics.  
- Detects quantities, units, ingredients, and steps.

### Image Generation / Image Service
- Generates a dish image from the recipe prompt using DALL·E, Stable Diffusion, etc.  
- Associates generated image path/URL with the recipe.

### Database & Persistence
- Stores parsed recipe, raw text, and image metadata in a database.  
- Uses SQLite or any relational DB for persistence.

### Workflow / Data Flow
```
User → LLM → Parser → DB → Image Service → Final Recipe Output
```

---

## Getting Started

### Prerequisites
- Python 3.8+  
- API key for LLM provider  
- Optional image generation API key

### Installation
```bash
git clone https://github.com/o0ga-bo0ga/Smart-Recipe-Generator.git
cd Smart-Recipe-Generator
pip install -r requirements.txt
```

### Configuration / Environment Variables
```
LLM_API_KEY=your_openai_api_key
IMAGE_API_KEY=your_image_api_key
DATABASE_URL=sqlite:///recipes.db
```

### Running the App
```bash
python app.py
```

---

## Usage
1. Enter ingredients.  
2. Generate recipe.  
3. View structured data and dish image.  
4. Save recipe for later access.

---

## Project Structure
```
Smart-Recipe-Generator/
├── app.py
├── llm_service.py
├── recipe_parser.py
├── image_service.py
├── db_service.py
├── requirements.txt
├── recipes.db
├── templates/
├── static/
├── data/
├── results/
└── README.md
```

---
