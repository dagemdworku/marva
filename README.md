# Marva

Marva is an AI-powered marketing platform designed to assist businesses with marketing strategy, content creation, and social media management. It leverages advanced AI agents integrated via LangChain and Ollama to automate and optimize marketing workflows.

![Marva AI Screenshot](images/marva-screenshot.png "Marva AI Screenshot")

## Features

- **Marketing Strategist Agent**: Analyzes company bio and post analytics to create targeted marketing strategies.
- **Marketing Material Creator Agent**: Reads company materials and existing posts/comments to generate new marketing content.
- **Social Media Analyzer & Post Replier Agent**: Summarizes social media data and provides insights.
- **Post Replier Agent**: Generates replies to posts and comments.
- **Lightweight Local Database**: Uses SQLite for storing posts, comments, and chat conversations.
- **Interactive Chat Interface**: Communicate with AI agents to receive insights, strategies, and content suggestions.
- **Admin Dashboard**: Built-in Django admin to view and manage database content effortlessly.

## Technology Stack

- **Backend**: Django 5.2.1
- **AI Integration**: LangChain 0.3.25 with Ollama and OpenAI
- **Database**: SQLite (file-based relational database)
- **PDF Processing**: PyPDF2
- **Environment Management**: python-dotenv
- **Other Tools**: Pandas for data manipulation

## Installation and Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/dagemdworku/marva.git
   cd marva
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables (optional)**

   Create a .env file in the root directory and add your OpenAI API key if available:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   If no OpenAI API key is found, the system will default to using Ollama.

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the application**

   Open your browser and navigate to http://127.0.0.1:8000

7. **Access the admin panel**

   Open your browser and navigate to http://127.0.0.1:8000/admin/
   and use the following super user login credentials:

   - username `dagemdworku`
   - password `password`

   ...or run the following command to create a new super user

   ```bash
   python manage.py createsuperuser
   ```

## Project Structure

```bash
   marva/
    ├── .venv/                  # Python virtual environment (not committed to git)
    ├── .vscode/                # VS Code editor settings and workspace configuration
    ├── core/                   # Main Django app with models, views, and AI agents
    ├── node_module/            # Node.js dependencies for frontend tooling
    ├── marva/                  # Django project settings
    ├── static/                 # Static files (CSS, JS, images)
    ├── manage.py               # Django project management script
    ├── requirements.txt        # Project dependencies
    ├── company_bio.pdf         # Example company bio PDF for AI agents
    ├── db.sqlite3              # SQLite database file
    ├── input.css               # Source CSS for Tailwind
    ├── package.json            # Node.js project metadata and scripts
    ├── tailwind.config.js      # Tailwind CSS configuration (added for VS Code extension to work)
    ├── README.md               # Project documentation
    ├── .gitignore              # Git ignore rules
    └── .env                    # Environment variables
```

## Development

- **Run Tailwind CSS CLI**

  ```bash
  npx @tailwindcss/cli -i input.css -o static/css/output.css --watch
  cd marva
  ```

- **Run database migrations**

  ```bash
  python manage.py migrate
  ```

- **Insert Seed Data**

  The `seed_csv` management command populates the database with initial data from CSV files.

  ```bash
  python manage.py seed_csv
  ```

## Testing

Unit tests are implemented for core functionalities and AI agent interactions. To run tests:

```bash
python manage.py test
```

## Contribution

Contributions, suggestions, and improvements are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, reach out to Dagem D Worku (Dagi).

dagemdworku@gmail.com
