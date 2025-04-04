# System Flow Diagram

## User Journey and System Flow

```mermaid
graph TD
    A[User] -->|1. Initial Request| B["/prompt Endpoint"]
    B -->|2. Input Data| C{Process Request}
    
    subgraph InputData
        D[Images] --> C
        E[Colors Palette] --> C
        F[Offer Details] --> C
        G[Theme] --> C
    end

    C -->|3. Initial Processing| H[Gemini AI]
    H -->|4. Generate| I[Product Details]
    
    subgraph ProductDetails
        J[Product Name] --> I
        K[Product Description] --> I
        L[Color Scheme] --> I
    end

    I -->|5. Stage 1| M[Generate Stage 1 Prompt]
    M -->|6. Process| N[Gemini Response]
    N -->|7. Stage 2| O[Generate Final Prompt]
    
    O -->|8. Image Generation| P[Imagen Service]
    P -->|9. Return| Q[Generated Images]
    
    Q -->|10. Final Response| R[Response to User]

    %% Chatbot Flow
    A -->|11. Chat Request| S["/chat-bot Endpoint"]
    S -->|12. Process| T{Check Type}
    T -->|Text Only| U[Gemini Text Response]
    T -->|With Image| V[Gemini + Imagen]
    U -->|13. Return| W[Text Response]
    V -->|14. Return| X[Text + Image Response]
```

## Detailed Flow Explanation

### 1. Initial Request Flow
1. **User Input**
   - Uploads product images
   - Provides color palette
   - Specifies offer details
   - Selects theme

2. **Data Processing**
   - System validates input
   - Processes images
   - Prepares data for AI processing

### 2. AI Processing Flow
1. **Initial Analysis**
   - Gemini AI analyzes images
   - Generates product details
   - Creates initial prompts

2. **Two-Stage Prompt Generation**
   - Stage 1: Basic product description
   - Stage 2: Detailed marketing content

### 3. Image Generation Flow
1. **Final Prompt Creation**
   - Combines all parameters
   - Optimizes for image generation

2. **Image Generation**
   - Imagen service creates images
   - System processes and validates output

### 4. Chatbot Flow
1. **User Interaction**
   - Text-based queries
   - Image generation requests

2. **Response Generation**
   - Text-only responses
   - Combined text and image responses

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Backend
    participant Gemini
    participant Imagen
    
    User->>Backend: Send Request (/prompt)
    Backend->>Gemini: Process Images
    Gemini-->>Backend: Return Product Details
    Backend->>Gemini: Generate Stage 1 Prompt
    Gemini-->>Backend: Return Stage 1 Response
    Backend->>Gemini: Generate Stage 2 Prompt
    Gemini-->>Backend: Return Final Prompt
    Backend->>Imagen: Generate Images
    Imagen-->>Backend: Return Generated Images
    Backend-->>User: Return Complete Response
```

## File Structure

```
backend/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── .env                  # Environment variables
├── src/
│   ├── flow_after_imagegen.py  # Post-generation flow
│   ├── gemini_utils.py         # Gemini AI integration
│   ├── imagen.py              # Image generation
│   └── prompts.py             # Prompt templates
├── semantic_search.py    # Search functionality
└── gemini_file.py       # Additional Gemini utilities
```

## Key Components Interaction

```mermaid
graph LR
    A[Flask App] --> B[Gemini AI]
    A --> C[Imagen Service]
    B --> D[Prompt Generation]
    C --> E[Image Generation]
    D --> E
    E --> F[Final Output]
```

## Error Handling Flow

```mermaid
graph TD
    A[Request] --> B{Validate Input}
    B -->|Invalid| C[Return 400 Error]
    B -->|Valid| D{Process Request}
    D -->|AI Error| E[Return 500 Error]
    D -->|Image Gen Error| F[Return 500 Error]
    D -->|Success| G[Return Response]
``` 