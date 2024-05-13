# Up Your English
Enhance your English proficiency with our comprehensive tool. This application combines the power of modern technologies and artificial intelligence to provide an interactive learning experience.

## Screenshots

![Screenshot](https://github.com/vsdudakov/up_your_english/blob/main/screenshot.png)



## Quickstart
 - Running the Project with Docker
 - Execute the following command to build and run the project:

```bash
export OPENAI_API_KEY=<your_key>
docker compose up --build
```

 - Access the application by navigating to: http://localhost:5137

## Continuous Integration (CI)
### Overview
We utilize GitHub Actions to automate our testing and integration processes.

### Backend
 - Tools: Ruff (black, isort, flake8), Pytest
 - Operations: Automated testing is performed on each push and pull request.
### Frontend
 - Tools: Biome, ESLint, Jest
 - Operations: Automated testing is performed on each push and pull request.

## Architecture
### Backend
 - Framework: FastAPI/Python, Redis
 - Structure: MVC architecture (Endpoint -> Service -> Adapters)
 - Features:
   - REST API and Websockets for asynchronous chat functionalities.
   - Redis queue with brpop to handle websocket messages.
   - Session management using cookies.
 - Libraries: Utilizes LangChain and OpenAI for AI-driven operations, streaming responses via websockets to the React client.
### Frontend
 - Framework: Vite / React, TypeScript
 - UI Components: Ant Design (Antd)
 - Chat: react-chat-components library
 - State Management: React Query, React Use Websocket, Context Providers

## Roadmap
### Testing:
 - Add unit tests for the backend with Pytest.
 - Incorporate smoke tests for the frontend using Jest.
 - Develop automated tests with Playwright for end-to-end testing.
### Deployment:
 - Implement Continuous Deployment (CD) with GitHub Actions, enabling deployment via releases or manual triggers.
### Infrastructure:
 - Decouple adapters and backend API logic into a microservice architecture, potentially utilizing Kafka or RabbitMQ.
 - Implement authentication enhancements using HTTP-only cookies or JWT tokens for mobile.
 - Integrate a database to persist chat history and other relevant data.
### AI Enhancements:
 - Enhance AI functionalities to support multiple prompts within a single session.


This revised README is designed to provide a clear, professional description of your project, its current capabilities, and future development plans. The sections are organized to guide readers easily from setup instructions to deeper technical details.





