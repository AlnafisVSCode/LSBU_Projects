import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
import json
import os

def extract_text_from_pdf(file_path, keywords):
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            total_occurrences = {category: {word: 0 for word in words} for category, words in keywords.items()}
            for i in range(len(reader.pages)):  # Iterate over all pages
                page = reader.pages[i]
                text = page.extract_text()
                for category, words in keywords.items():
                    for word in words:
                        total_occurrences[category][word] += text.count(word)
            return total_occurrences

    except FileNotFoundError:
        return f"Error: The file {file_path} was not found."
    except OSError:
        return f"Error: Could not read the file {file_path}. It may be corrupted or unreadable."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def read_cumulative_counts(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {"Physical exposure": {}, "Policy related": {}}

def save_cumulative_counts(counts, file_path):
    with open(file_path, 'w') as file:
        json.dump(counts, file, indent=4)
    print(f"Cumulative counts saved to {file_path}")

def plot_occurrences(total_occurrences):
    words = [f"{category}: {word}" for category, words in total_occurrences.items() for word in words]
    counts = [count for category in total_occurrences.values() for count in category.values()]

    plt.figure(figsize=(10, 6))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    wedges, texts, autotexts = plt.pie(counts, labels=words, autopct='%1.1f%%', startangle=140, colors=colors)
    
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    plt.title('Occurrences of Keywords in PDF', fontsize=14, weight='bold', pad=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.legend(wedges, words, title="Keywords", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.show()

def process_pdf_file():
    file_path = 'Reports/LSE/Annual reports/LSE_ULVR_2012.pdf'
    cumulative_counts_path = 'cumulative_counts.json'
    keywords = {
        "Physical exposure": [
            "climate change", "weather", "extreme weather", "weather events", "Warming", "Temperature",
            "Extreme temperature", "heatwave", "heating season", "severe winter", "mild winter", 
            "normal winter", "winter conditions", "coldwave", "Flooding", "the flood", "the floods", 
            "tsunami", "high water", "drought", "droughts", "water scarcity", "water stress", 
            "precipitation", "rainfall", "Physical Environmental", "hurricane", "hurricanes", 
            "storms", "storm related", "storm losses", "storm activity", "tropical storm", "the snow", 
            "snowfall", "snowstorm", "the ice", "wildfire", "wildfires", "air quality", "air pollutants", 
            "degree days", "polar vortex", "greenhouse gas"
        ],
        "Policy related": [
            "Carbon tax", "Voluntary removal costs", "Net zero", "Net-zero", "Net-zero GHG emissions", 
            "Forest", "Energy transition", "Adaptation", "Mitigation"
        ]
    }
    
    current_run_counts = extract_text_from_pdf(file_path, keywords)
    
    if isinstance(current_run_counts, str):
        print(current_run_counts)  # Print error messages directly
        return
    
    cumulative_counts = read_cumulative_counts(cumulative_counts_path)
    
    # Ensure cumulative_counts structure is correct
    for category in keywords:
        if category not in cumulative_counts:
            cumulative_counts[category] = {}
        for word in keywords[category]:
            if word not in cumulative_counts[category]:
                cumulative_counts[category][word] = 0

    # Update cumulative counts with current run counts
    for category, words in current_run_counts.items():
        for word, count in words.items():
            cumulative_counts[category][word] += count
    
    save_cumulative_counts(cumulative_counts, cumulative_counts_path)
    
    print("Cumulative occurrences:")
    for category, words in cumulative_counts.items():
        print(f"\n{category}:")
        for word, count in words.items():
            print(f"{word}: {count}")
    
    plot_occurrences(cumulative_counts)

# Run the functions
process_pdf_file()
