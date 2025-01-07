# Streamlit Israel-Gaza War Data Visualization (October 7 War)

This project provides an interactive dashboard to visualize and analyze the casualties data from the Israel-Gaza conflict, specifically from the October 7, 2023, war. The data is fetched daily and presented with insights such as total casualties, average deaths, and casualty proportions, as well as daily updates on the situation.

![image](https://github.com/user-attachments/assets/2d8c2ef3-18b2-4131-9b29-2f2e8df9e187)

## Features

- **Casualty Statistics**: View daily, cumulative, and categorized casualty information (killed, injured, by gender, by age).
- **Casualty Proportions**: View the distribution of casualties by gender (women, children, men) and profession (medical personnel, journalists).
- **Charts and Graphs**: Visualizations of daily casualties, cumulative figures, and pie charts showing casualty distribution by gender.
- **Recent Data**: View the most recent 10 days of casualty data and trends.
- **Data Summary**: Aggregate data including total casualties, number of women, men, children killed, etc.

## Prerequisites

To run this project, you need to have the following Python libraries installed:
- `streamlit`
- `pandas`
- `requests`
- `matplotlib`

You can install them using pip:

```bash
pip install streamlit pandas requests matplotlib
```

## Getting Started

1. **Clone this repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/Israel-Gaza-War.git
   cd Israel-Gaza-War
   ```

2. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

   This will start the dashboard in your default web browser.

## How It Works

1. **Data Downloading and Processing**: The application downloads the casualty data from a public API and stores it in a CSV file (`War.csv`). If the data cannot be fetched, it will use a cached version of the data if available.
   
2. **Data Visualization**:
   - The main page displays an interactive dashboard with graphs showing daily casualties, cumulative deaths, and injury data.
   - A pie chart breaks down the casualties into different categories, such as children, women, and men killed.
   - A bar chart shows the average daily number of deaths, categorized by gender.
   
3. **Sidebar**: The sidebar contains:
   - **Casualties Summary**: The total number of people killed, injured.
   - **Last 10 Days Data**: A quick summary of casualties over the last 10 days.
   - **Daily Trends**: Graphs that show trends over the course of the war.

## Project Structure

```
Israel-Gaza-War/
│
├── app.py                  # Main Streamlit app
├── War.csv                 # Cached data file (if data is fetched successfully)
└── README.md               # Project documentation
```

## License

This project is open-source and available under the MIT License.

## Acknowledgments

- The data used in this project is sourced from the [Tech for Palestine API](https://data.techforpalestine.org).
- This project was developed by AL-Hassan Sarrar (@s4rrar).
