# LinkedIn Content Automation Agent

A powerful LinkedIn automation tool that helps you generate, schedule, and post engaging content to your LinkedIn profile with AI assistance.

![Dashboard Preview](https://via.placeholder.com/800x400.png?text=LinkedIn+Agent+Dashboard)

## ✨ Features

- **AI-Powered Content Generation**
  - Generate professional LinkedIn posts using OpenAI
  - Customize content based on topics and preferences
  - Support for image uploads with generated content

- **Scheduling System**
  - Schedule posts for optimal engagement times
  - Background scheduler for automated posting
  - Easy approval workflow for content review

- **Analytics & Export**
  - Track post performance
  - Export post history to CSV
  - Monitor engagement metrics

- **Smart Automation**
  - Auto-comment on your own posts
  - Engage with other relevant content
  - Promotion management tools

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- LinkedIn Developer Account
- OpenAI API Key

### Installation

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd Linky
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the `linkedin_agent` directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LINKEDIN_CLIENT_ID=your_linkedin_client_id
   LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
   LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
   SECRET_KEY=your_secret_key
   ```

### Running the Application

1. Initialize the database:
   ```bash
   alembic upgrade head
   ```

2. Start the application:
   ```bash
   uvicorn linkedin_agent.app:app --reload
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## 🛠️ Usage

1. **Configure Your Settings**
   - Navigate to `/settings`
   - Enter your profile information
   - Configure automation preferences

2. **Generate Content**
   - Go to the dashboard
   - Enter a topic for your post
   - Choose to add an image
   - Schedule for later or post immediately

3. **Review & Approve**
   - Preview generated content
   - Make edits if needed
   - Approve for posting

## 📊 Features in Detail

### Dashboard
- View scheduled and published posts
- Quick access to content generation
- Performance metrics at a glance
  <img width="1600" height="1000" alt="image" src="https://github.com/user-attachments/assets/86902d11-89b4-4761-ace3-37c2073ba2ab" />


### Content Generation
- AI-powered post creation
- Customizable tone and style
- Image upload and management

### Scheduling
- Calendar view of scheduled posts
- Best time to post recommendations
- Bulk scheduling options

### Analytics
- Engagement metrics
- Follower growth tracking
- Exportable reports

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

💡 **Tip**: For best results, regularly update your content strategy based on the analytics provided by the platform.
