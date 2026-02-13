# 🚀 ZotifyFrontEnd

<div align="center">


[![GitHub stars](https://img.shields.io/github/stars/m335671/ZotifyFrontEnd?style=for-the-badge)](https://github.com/m335671/ZotifyFrontEnd/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/m335671/ZotifyFrontEnd?style=for-the-badge)](https://github.com/m335671/ZotifyFrontEnd/network)
[![GitHub issues](https://img.shields.io/github/issues/m335671/ZotifyFrontEnd?style=for-the-badge)](https://github.com/m335671/ZotifyFrontEnd/issues)
[![GitHub license](https://img.shields.io/github/license/m335671/ZotifyFrontEnd?style=for-the-badge)](LICENSE) <!-- TODO: Add LICENSE file if available -->

**A minimalist web interface for your local Zotify instance.**


</div>

## 📖 Overview

ZotifyFrontend is a simple interface to interact with the Zotify tool on your system

## ✨ Features

- 🎯 **Simple & Intuitive Interface:** A clean design focused on ease of use.
- 🔗 **Connect to Local Zotify:** Seamless integration with your existing Zotify backend instance.
- 🌐 **Web-Based Accessibility:** Access your Zotify controls from any browser.
- ⚙️ **Basic Zotify Interaction:** Provides essential controls to manage your Zotify system.

## 🛠️ Tech Stack

**Frontend:**

  ![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Backend:**

  ![Static Badge](https://img.shields.io/badge/Python-white?style=for-the-badge&logo=python&logoColor=white&color=yellow)

## 💻 Installation

Follow these steps to get ZotifyFrontEnd up and running locally.

### Prerequisites
Before you begin, ensure you have the following installed:
- **Node.js**
- **npm**
- **The Zotify Tool installed AND globally available on your device**: The Zotify tool must be Available for the Backend to function (See : ![INSTALLATION](https://github.com/m335671/ZotifyForkForked/blob/main/INSTALLATION.md) in my own repo or in any ![FUNCTIONAL](https://github.com/Googolplexed0/zotify) zotify Repo).
- **A valid Spotify Client-id** : As for any currently working Zotify tool you will need a  `Client ID` (See [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)).
### ⚠️Due To Recent Api updates you now need a Spotify Premium Account to get a client-ID ⚠️ 


### running the app

1. **Clone the repository**
   ```bash
   git clone https://github.com/m335671/ZotifyFrontEnd.git
   cd ZotifyFrontEnd
   ```

2. **Run The Backend**
    ```bash
    # Go to the Backend Folder
    cd Backend
        
    # Create a virtual environement (Optional but recommended)
    python -m venv venv
        
    # Activate the environement
    # On Windows :
        .\venv\Scripts\activate.bat
    # ON Linux/Mac :
    ## Not yet Tested
        
    # Install the dependencies
    pip install fastapi uvicorn
        
    # Start the Backend Server
    uvicorn main:app --reload --port 1337
    ```

3. **Install dependencies**
   ```bash
   # Go to the Frontend Folder
   cd Frontend

   # Install the dependencies
   npm install
      
   # Start the frontend
   npm run dev
   ```

4. **Open your browser**
   Visit `http://localhost:5173` (or the port indicated in your terminal) to view the application.

## 🗺️ RoadMap

- [ ] **Add multiple languages** : Add languages for the app. (Currently only French and English are available)
- [ ] **Docker** : Create a single container including Zotify, the backend, and the frontend.
- [ ] **Linux support** : Improve system command compatibility for Unix environments. (Not yet Tested)
- [ ] **Queue manager** : Implement a robust queue to automatically handle Zotify's “single-task” limitations.
- [ ] **Design** : Improve user Interface style and readability


## 🤝 Contributing

We welcome contributions on ZotifyFrontEnd! If you're interested in improving this project, please consider the following:

### Translation

   If you can Translate the app ! Please follow theses steps :

  - **Fork the repository.**
  - Modify the translation.js file
  - Submit a pull request with the language you just added

### Bug fixes

   If you want to fix a bug ! Please follow theses steps :

  - **Fork the repository.**
  - Make your changes and ensure they adhere to the project's coding style.
  - Submit a pull request with a clear description of your changes.

## 🙏 Acknowledgments

- Built with [Vue.js](https://vuejs.org/)
- Powered by [Vite](https://vitejs.dev/) for a fast development experience.
- Relies on the core functionalities provided by the Zotify app.

## 📞 Support & Contact

- 🐛 Issues: Please report any bugs or feature requests on the [GitHub Issues page](https://github.com/m335671/ZotifyFrontEnd/issues).
- 📧 Contact: For any other inquiries, you can reach out to the repository owner `m335671` via GitHub.

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [m335671](https://github.com/m335671)

</div>
