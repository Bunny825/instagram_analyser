# AI Instagram Channel Analyzer

This project is a full-stack application that analyzes an Instagram account, provides AI-driven content insights, and generates a new post idea complete with a unique thumbnail.


NOTE:As in the document of the plan you specified, i have only taken my facebook page and instagram bussiness account then created the Instagram graph API key just for my account as you have specified.I want to mention again that we can have a mechanism that can access the instagram channel of anyone and can then analyse but for that we need OAuth 2.0 which is complex is also out of the scope of GenAI and the main Aim of this project.


## The Process Flow

The application provides a seamless experience for the user by coordinating a frontend interface with a powerful backend API. Here is the step-by-step flow:

### 1. Kicking off the Analysis

The process begins on the Streamlit web interface. The user enters the name of an Instagram channel and clicks "Analyze." This action triggers the frontend to send a request to the FastAPI backend, initiating the data collection process.

### 2. Data Collection

The backend receives the request and calls the official Instagram Graph API. It fetches the latest profile data (username, follower count) and recent media (captions, likes, comments). This live data is then saved locally as a JSON file, which serves as the single source of truth for the rest of the analysis. If the live API fails, the system gracefully falls back to using pre-existing mock data to ensure functionality.

### 3. Generating AI-Powered Insights

Once the data is stored, the frontend makes two more requests to the backend to generate insights using the Google Gemini API:

-   **Performance Summary**: The `/summarize` endpoint is called. The backend creates a prompt with key statistics (follower count, total likes, etc.) and asks Gemini to produce a concise, analytical summary of the account's performance.

-   **Post Recommendation**: The `/recommend` endpoint is called. The backend creates a more detailed prompt, including a breakdown of recent posts and their engagement metrics (likes and comments). It instructs the AI to act as a social media strategist, identify successful content patterns, and suggest a new post complete with a caption, relevant hashtags, and a justification for why it would perform well.

### 4. Visualizing the Content Idea

The frontend receives the summary and recommendation and displays them in a clean, two-column layout. The user can now review the AI's strategic advice. At this stage, a new button, "Generate Thumbnail," appears below the recommended post.

### 5. AI Image Generation

When the user clicks "Generate Thumbnail," the frontend sends the AI-generated caption to the backend's `/generate-thumbnail` endpoint. The backend uses this caption to create a detailed prompt for the OpenAI DALL-E 3 API, which generates a high-quality, unique image. The backend then downloads this image and saves it to a local `outputs` folder.

### 6. Displaying the Final Result

The backend responds to the frontend with a unique URL pointing to the locally saved image. The Streamlit application then displays this final image, completing the workflow from data analysis to a fully-realized content idea.

## Technical Overview

-   **Backend**: FastAPI, Python
-   **Frontend**: Streamlit, Python
-   **AI Text Generation**: Google Gemini
-   **AI Image Generation**: OpenAI DALL-E 3

## How to Run

1.  **Setup**:
    - Clone the repository.
    - Create a Python virtual environment and activate it.
    - Create a `.env` file and add your `INSTAGRAM_API_TOKEN`, `GEMINI_API_KEY`, and `OPENAI_API_KEY`.
    - Install dependencies: `pip install -r requirements.txt`.

2.  **Execution**:
    - **Start Backend**: In a terminal, run `uvicorn backend.main:app --reload`.
    - **Start Frontend**: In a second terminal, run `streamlit run frontend/app.py`.