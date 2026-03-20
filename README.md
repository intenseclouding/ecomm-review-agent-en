# 🛍️ E-commerce Review Analysis System

An AI agent-based e-commerce review analysis and management system. It leverages the Strands framework and Claude Sonnet to provide features such as review moderation, keyword extraction, sentiment analysis, and auto-response, and also offers hands-on experience with Agent deployment and operations through AgentCore.

## 📋 Project Overview

This project is a system that automatically analyzes and manages customer reviews on e-commerce platforms using AI. Each Lab handles an independent function and implements progressively more complex AI agent capabilities step by step.

### 🎯 Key Objectives
- **Review Quality Management**: Automated moderation of inappropriate reviews
- **Customer Insight Extraction**: Deriving product improvement points through keyword and sentiment analysis
- **Customer Service Automation**: AI-based auto-response system
- **Unified Management**: Orchestration of all analysis functions
- **Cloud Deployment**: Production deployment via Amazon Bedrock AgentCore

## 🏗️ Project Structure

```
📦 ecomm-review-agent/
├── 📁 lab01_review_sentiment_analyzer/ # Sentiment Analysis System
├── 📁 lab02_review_keyword_extractor/  # Keyword Extraction System
├── 📁 lab03_review_moderator/          # Review Moderation System
├── 📁 lab04_review_auto_response/      # Auto Response System
├── 📁 lab05_orchestrator/              # Unified Orchestrator
├── 📁 images/                          # Test images
├── 📄 requirements.txt                 # Project dependencies
├── 📄 setup_venv.sh                    # Virtual environment setup script
└── 📄 README.md                        # This file
```

## 🚀 Detailed Lab Descriptions

### Lab 01: Sentiment Analyzer ✅
**Completion: 100%**

A system that analyzes review sentiment to determine positive/negative/neutral.

**Key Features:**
- Hybrid sentiment analysis (LLM + dictionary-based)
- Recognition of internet slang and neologisms
- Confidence score provided
- Analysis path tracking (llm/llm→dict/dict_fallback)

**How to Run:**
```bash
cd lab01_review_sentiment_analyzer
streamlit run streamlit_app.py
```

**Highlights:**
- Supports internet slang such as "love it", "awesome", "no hope", "total disaster", etc.
- Automatically triggers dictionary-based re-analysis when LLM is uncertain
- Provides detailed analysis rationale

**Recent Improvements:**
- Agent logic improvements and optimization
- UI updates for better usability

---

### Lab 02: Keyword Extractor ✅
**Completion: 100%**

A system that automatically extracts product-related keywords from reviews.

**Key Features:**
- Product attribute keyword extraction (sound quality, battery, comfort, etc.)
- Keyword-based related review search
- Database storage and management
- Agent debugging information provided

**How to Run:**
```bash
cd lab02_review_keyword_extractor
streamlit run streamlit_app.py
```

**Highlights:**
- Extracts only up to 3 core keywords
- Excludes emotional expressions (objective attributes only)
- Specialized keyword dictionary

**Recent Improvements:**
- Changed from JSON format to TXT format (registered_keywords.json → registered_keywords.txt)
- Simplified keyword management and improved readability

---

### Lab 03: Review Moderator ✅
**Completion: 100%**

A system that automatically moderates inappropriate reviews.

**Key Features:**
- Profanity/explicit content detection
- Image-text matching verification
- Star rating-content consistency analysis
- Comprehensive PASS/FAIL determination

**How to Run:**
```bash
cd lab03_review_moderator
streamlit run streamlit_app.py
```

**Technologies Used:**
- Strands Agent Framework
- Claude 3.7 Sonnet
- PIL-based image analysis
- SQLite database

**Recent Improvements:**
- Switched to PIL (Python Imaging Library) based approach
- Improved to single image support
- Optimized image processing performance

---

### Lab 04: Auto Response ✅
**Completion: 80%**

A system that generates AI-based automatic responses to customer reviews.

**Key Features:**
- Customized responses based on review sentiment
- Brand tone and manner reflection
- Customer satisfaction-enhancing response generation
- Response quality evaluation system

**How to Run:**
```bash
cd lab04_review_auto_response
streamlit run streamlit_app.py
```

**Tech Stack:**
- Strands Agent + Claude 3.7
- Response template system
- Brand guideline compliance

**Recent Improvements:**
- Simplified UI and removed unnecessary features
- Improved auto-response logic

---

### Lab 05: Orchestrator ✅
**Completion: 90%**

A system that integrates all analysis functions to provide an automated workflow.

**Key Features:**
- Automatically runs all analyses when a review is submitted
- Sequential execution: Sentiment Analysis → Keyword Extraction → Moderation → Auto Response
- Integrated result visualization through dashboard
- Sub-agent based architecture

**How to Run:**
```bash
cd lab05_orchestrator
streamlit run streamlit_app.py
```

**Tech Stack:**
- Multi-Agent orchestration
- Sub-agent pattern (sentiment_analyzer, keyword_extractor, review_moderator, auto_responser)
- Data pipeline management
- Real-time monitoring

**Recent Improvements:**
- Improved Orchestrator structure
- Sub-agents integration and optimization
- Completed comprehensive review analysis workflow

## 🛠️ Installation and Setup

### 1. Automatic Setup (Recommended)

```bash
# Automatically create virtual environment and install dependencies
./setup_venv.sh
```

### 2. Manual Setup

```bash
# Requires Python 3.8+
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running

Each Lab can be run independently:

```bash
# Run Lab 01 (Sentiment Analysis)
cd lab01_review_sentiment_analyzer && streamlit run streamlit_app.py

# Run Lab 02 (Keyword Extraction)
cd lab02_review_keyword_extractor && streamlit run streamlit_app.py

# Run Lab 03 (Review Moderation)
cd lab03_review_moderator && streamlit run streamlit_app.py

# Run Lab 04 (Auto Response)
cd lab04_review_auto_response && streamlit run streamlit_app.py

# Run Lab 05 (Orchestrator)
cd lab05_orchestrator && streamlit run streamlit_app.py
```

## 📊 Test Data

Each system includes the following sample data:

- **Positive Review**: "This product is really great! The sound quality is excellent and the battery lasts a long time."
- **Negative Review**: "Total garbage. A complete waste of money."
- **Review with Image**: Provided with flower photos and earphone photos
- **Internet Slang**: "love it", "awesome", "no hope", "total disaster", etc.

## 🎯 Current Development Status

| Lab | Feature | Status | Completion |
|-----|---------|--------|------------|
| Lab 01 | Sentiment Analysis | ✅ Complete | 100% |
| Lab 02 | Keyword Extraction | ✅ Complete | 100% |
| Lab 03 | Review Moderation | ✅ Complete | 100% |
| Lab 04 | Auto Response | ✅ Nearly Complete | 80% |
| Lab 05 | Orchestrator | ✅ Nearly Complete | 90% |

## 📝 TODO & Roadmap

### 🔥 High Priority
- [ ] **Complete Lab 4 (Auto Response)**
  - [x] Implement basic auto-response logic
  - [x] Simplify UI
  - [ ] Add response quality evaluation metrics (20%)

- [ ] **Complete Lab 5 (Orchestrator)**
  - [x] Design Multi-Agent workflow
  - [x] Integrate Sub-agents (sentiment_analyzer, keyword_extractor, review_moderator, auto_responser)
  - [x] Develop integrated dashboard UI
  - [ ] Implement batch processing system (10%)

### 🚀 Production Deployment
- [ ] **AWS Bedrock AgentCore Deployment**
  - [ ] Bedrock AgentCore integration design
  - [ ] Cloud architecture configuration
  - [ ] API Gateway & Lambda setup
  - [ ] DynamoDB schema design

### ⚡ Performance Improvements
- [ ] **Asynchronous Multi-Review Processing System**
  - [ ] Implement SQS-based queue system
  - [ ] Optimize parallel processing
  - [ ] Real-time monitoring dashboard
  - [ ] Automated throughput scaling

### 🔧 Technical Improvements
- [x] Add project configuration files (requirements.txt, setup_venv.sh)
- [ ] Enhance error handling and resilience
- [ ] Performance monitoring and logging system
- [ ] Add unit tests and integration tests
- [ ] Database migration system
- [ ] Security hardening (API key management, data encryption)

## 🤝 How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📚 References

- [Strands Framework Documentation](https://strands.ai)
- [Claude 3.7 Sonnet API](https://docs.anthropic.com)
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock)
- [Streamlit Documentation](https://docs.streamlit.io)

## 📄 License

MIT License - See the [LICENSE](LICENSE) file for details.

---

**Developer**: YejinKM
**Version**: 2.0.0
**Last Updated**: October 2025

## 📌 Recent Changes (v2.0.0)

- Overall improvements and optimization for Labs 01-05
- Lab structure reorganization (changed order to: Sentiment Analysis → Keyword Extraction → Moderation)
- Project setup automation (added requirements.txt, setup_venv.sh)
- Lab 04 Auto Response system implementation (80% complete)
- Lab 05 Orchestrator Sub-agent architecture implementation (90% complete)
- Keyword management system improvement (JSON → TXT)
- Switched to PIL-based image processing

> 💡 **Tip**: Each Lab can be run independently, but it is recommended to try them sequentially for a full understanding of the overall system.
