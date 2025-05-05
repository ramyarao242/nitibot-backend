# Prerequisite: pip install sentence-transformers
"""
	This script loads verses from 'chanakya_neeti_all_chapters.json', computes their sentence embeddings using
	the 'all-MiniLM-L6-v2' model, and saves the enriched data with an 'embedding' field for each verse
	to 'chanakya_verses_with_embeddings.json'.

	Make sure to install the sentence-transformers library before running (e.g., via pip).
"""
import json
print("started embeddings")
from sentence_transformers import SentenceTransformer

def main():
	print("started embeddings")
	# Define input and output file paths
	input_path = "chanakya_neeti_all_chapters.json"
	output_path = "chanakya_verses_with_embeddings.json"
	print("started embeddings")

	# Load the Chanakya Neeti verses data from the JSON file
	with open(input_path, "r", encoding="utf-8") as f:
		data = json.load(f)

	# Initialize the sentence-transformer model (all-MiniLM-L6-v2)
	model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
	print("model downloaded successfully")

	# Prepare a list of verse entries regardless of the JSON structure (flat list or chapters)
	verses_list = []
	if isinstance(data, list):
		# If data is a list of chapters (each with a 'verses' list), gather all verses
		if data and isinstance(data[0], dict) and "verses" in data[0]:
			for chapter in data:
				verses_list.extend(chapter.get("verses", []))
		else:
			# Data is already a flat list of verse dictionaries
			verses_list = data
	elif isinstance(data, dict):
		# If data is a dict with a 'verses' list (or a dict of verses), handle accordingly
		if "verses" in data and isinstance(data["verses"], list):
				verses_list = data["verses"]
		else:
			# If the dict is a collection of verse entries, take the values
			for value in data.values():
				if isinstance(value, dict):
					verses_list.append(value)
					print("verses_list")
	else:
		print("Unsupported JSON structure for verses data.")
		raise ValueError("Unsupported JSON structure for verses data.")

	# Compute and add embeddings for each verse based on its English translation
	for verse in verses_list:
			# Use the English translation text for embedding (fallback to empty string if missing)
			english_text = verse.get("english") or verse.get("translation") or ""
			# Generate the embedding vector for the verse's English text
			embedding_vector = model.encode(english_text)
			# Convert to list if it's a NumPy array (for JSON serialization)
			verse["embedding"] = embedding_vector.tolist() if hasattr(embedding_vector, "tolist") else embedding_vector

	# Save the enriched data with embeddings to the output JSON file
	with open(output_path, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"Added embeddings for {len(verses_list)} verses. Saved results to '{output_path}'.")

if __name__ == "__main__":
	main()