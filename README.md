# HeyGen Video Generator

A Streamlit application that generates personalized video presentations using CV data and job descriptions. The app uses OpenAI's GPT-4 to create scripts and HeyGen's API to generate videos with avatars.

## Features

- PDF CV text extraction
- Automatic script generation based on CV, job description and a specific video question
- Video generation with customizable avatars, duration and language
- Status checking for generated videos
- Support for both English and Spanish content

## Prerequisites

- Python 3.8+
- OpenAI API key
- HeyGen API key

## Installation

1. Clone the repository:
git clone https://github.com/Jdaz1408/heygen-cv-video-generator.git
cd heygen-video-generato

2. Install the required packages:
pip install -r requirements.txt

3. Set up your environment variables: in the example.env file, replace the API_KEYGEN and OPENAI_API_KEY with your own keys.

4. Run the app:
streamlit run heygen.py

## Usage
0. Update your Avatar and Voice ID in the 'heygen.py' file
1. Upload your CV (PDF format)
   - The CV should be clearly formatted
   - Text should be selectable (not scanned images)
   - Recommended sections: Experience, Skills, Education

2. Enter the job description
   - Copy the full job posting
   - Include requirements and responsibilities

3. (Optional) Add a specific question
   - Default: "Why you are the best for the role"
   - Can be customized for different video purposes

4. Set video duration (1-10 minutes)

5. Generate and review the script

6. Send to HeyGen for video generation

7. Use the "Check Status" tab to monitor your video

## Privacy Considerations

- Do not commit your `.env` file
- Keep your CV private
- Video IDs are stored locally in `video_ids.txt`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to use this project for your own purposes. If you find it helpful, a link back to this repository would be appreciated but is not required.

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4o API
- [HeyGen](https://www.heygen.com/) for video generation API
- [Streamlit](https://streamlit.io/) for the web interface




