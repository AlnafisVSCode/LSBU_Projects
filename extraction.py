import asyncio
from PyPDF2 import PdfReader
import json
import aiofiles

async def extract_text_from_pdf(file_path):
    try:
        # Async file open
        async with aiofiles.open(file_path, 'rb') as file:
            content = await file.read()
            reader = PdfReader(content)
            results = []
            # Process only the first two pages
            for i in range(min(2, len(reader.pages))):
                page = reader.pages[i]
                text = page.extract_text()
                count = text.count('Brexit')
                results.append({
                    "page_number": i + 1,
                    "occurrences_of_brexit": count,
                    "extracted_text": text
                })
            return results

    except FileNotFoundError:
        return f"Error: The file {file_path} was not found."
    except OSError:
        return f"Error: Could not read the file {file_path}. It may be corrupted or unreadable."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

async def save_results_to_json(results, output_path):
    if isinstance(results, str):
        print(results)  # Print error messages directly
    else:
        async with aiofiles.open(output_path, 'w') as file:
            await file.write(json.dumps(results, indent=4))
        print(f"Results saved to {output_path}")

async def process_pdf_file():
    file_path = 'The Journal of Finance - 2023 - HASSAN - The Global Impact of Brexit Uncertainty.pdf'
    output_path = 'results.json'
    results = await extract_text_from_pdf(file_path)
    await save_results_to_json(results, output_path)

# Run the async function
asyncio.run(process_pdf_file())
