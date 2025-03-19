import os
import json

# Updated dataset with proprietary questions in the form of requests, troubleshooting instructions, and vendor contact information

knowledge_base_entries = [
    {
        "question": "Give me the current inventory for MX4500 chips.",
        "answer": "The current inventory for MX4500 chips at the Austin plant is 5,000 units.",
        "plant_location": "au_tx",
        "security": "Confidential",
        "groups": ["plant_managers_tx_us"]
    },
    {
        "question": "Give me the current inventory for MX4500 chips.",
        "answer": "The current inventory for MX4500 chips at the Berlin plant is 3,800 units.",
        "plant_location": "be_de",
        "security": "Confidential",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "How many robotic arm components are in stock at the Austin plant?",
        "answer": "The Austin plant has 200 robotic arm components in stock.",
        "plant_location": "au_tx",
        "security": "Confidential",
        "groups": ["plant_managers_tx_us"]
    },
    {
        "question": "How many robotic arm components are in stock at the Berlin plant?",
        "answer": "The Berlin plant has 200 robotic arm components in stock.",
        "plant_location": "be_de",
        "security": "Confidential",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "Give me the current inventory for ZM500 machine parts.",
        "answer": "The current inventory for ZM500 machine parts at the Berlin plant is 1,000 units.",
        "plant_location": "be_de",
        "security": "Confidential",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "Give me the current inventory for ZM500 machine parts.",
        "answer": "The current inventory for ZM500 machine parts at the Texas plant is 3,333 units.",
        "plant_location": "tx_us",
        "security": "Confidential",
        "groups": ["plant_managers_tx_us"]
    },
    {
        "question": "How many packing machine components are in stock at the Berlin plant?",
        "answer": "The Berlin plant has 150 packing machine components in stock.",
        "plant_location": "be_de",
        "security": "Internal",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "Give me the circuit board design for the MX4500 chip.",
        "answer": "The MX4500 chip design includes a 64-layer architecture with high-speed memory interfaces. The circuit board is designed to optimize signal integrity and reduce electromagnetic interference. Detailed design documentation includes PCB schematics, component placement, and routing strategies.",
        "security": "Confidential",
        "groups": ["plant_managers"]
    },
    {
        "question": "What if the robotic arm doesn't move",
        "answer": "If the robotic arm is unresponsive or doesn't move, then ensure the power supply is stable, and then perform a system reset by holding the reset button for 10 seconds.",

        "security": "Internal",
        "groups": ["plant_managers", "plant_operators_tx_us", "plant_operators_be_de"]
    },
    {
        "question": "If the conveyor belt stops, ensure the emergency stop is not engaged and restart the system.",
        "answer": "Check that the emergency stop button is disengaged, and press the 'Restart' button located on the main control panel to resume operations.",
        "plant_location": "au_tx",
        "security": "Internal",
        "groups": ["plant_managers_tx_us", "plant_operators_tx_us"]
    },
    {
        "question": "Give me the vendor contact information for replacement parts for the robotic arm.",
        "answer": "The vendor for robotic arm replacement parts is XYZ Robotics. Contact them at sales@robotics.com or +1-800-555-0101.",
        "plant_location": "au_tx",
        "security": "Confidential",
        "groups": ["plant_managers_tx_us"]
    },
    {
        "question": "Give me the machine settings for the ZM500 model.",
        "answer": "The ZM500 model machine settings include precise calibration data for speed control, torque adjustments, and sensor sensitivity settings. The proprietary configuration ensures optimal performance for manufacturing high-precision components. Documentation includes control parameters and tuning instructions.",
        "plant_location": "be_de",
        "security": "Confidential",
        "groups": ["plant_managers_be_de", "plant_managers_tx_us"]
    },
    {
        "question": "Give me the production protocols for the ZM500 model.",
        "answer": "The proprietary production protocols for the ZM500 model involve multi-stage quality checks, automated feedback systems for real-time error correction, and sensor-driven adjustments. The protocols ensure precision manufacturing and high throughput with minimal downtime. Detailed instructions cover setup and operational guidelines.",
        "plant_location": "be_de",
        "security": "Internal",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "If the packing machine jams, turn off the power and clear the obstruction before restarting.",
        "answer": "Switch off the power to the packing machine, remove any obstructions from the rollers, and restart the machine after clearing the jam.",
        "plant_location": "be_de",
        "security": "Internal",
        "groups": ["plant_managers_be_de", "plant_operators_be_de"]
    },
    {
        "question": "If the heating unit fails to maintain temperature, check the thermostat and replace any faulty sensors.",
        "answer": "Verify that the thermostat is set to the correct temperature, and if the issue persists, inspect and replace the faulty temperature sensors.",
        "plant_location": "au_tx",
        "security": "Internal",
        "groups": ["plant_managers_tx_us", "plant_operators_tx_us"]
    },
    {
        "question": "Give me the vendor contact information for replacement parts for the ZM500 machine.",
        "answer": "The vendor for ZM500 replacement parts is Acme Machines. Contact them at abc@acme.com or +49-30-123456.",
        "plant_location": "be_de",
        "security": "Confidential",
        "groups": ["plant_managers_be_de"]
    },
    {
        "question": "What is the global company-wide safety policy?",
        "answer": "All plants follow a global safety policy based on ISO 45001 standards, with specific local adaptations."
    }
]

output_dir = "documents"
os.makedirs(output_dir, exist_ok=True)

# Delete existing files ending with .txt in the output directory
for file in os.listdir(output_dir):
    if file.endswith(".txt"):
        os.remove(os.path.join(output_dir, file))

meta_data_list = []
document_count = 0
# Write the updated knowledge base entries to separate files
for entry in knowledge_base_entries:
    document_count += 1
    filename=f"document_{document_count}.txt"
    # Create the filename and write the content to the file
    file_path = os.path.join(output_dir, filename)

    # Write the content to the file
    with open(file_path, "w") as f:
        f.write(f"Question: {entry['question']}\n")
        f.write(f"Answer: {entry['answer']}\n")

    meta_data = {
        "source": file_path,
        "users": [],
        "metadata": {}
    }
    if "groups" in entry:
        meta_data["groups"] = entry["groups"]
    if "plant_location" in entry:
        meta_data["metadata"]["Plant"] = entry["plant_location"]
    if "security" in entry:
        meta_data["metadata"]["Security"] = entry["security"]
    meta_data_list.append(meta_data)

# Write the updated meta.json file

meta_file_path = os.path.join(output_dir, "meta.json")

with open(meta_file_path, "w") as meta_file:
    json.dump(meta_data_list, meta_file, indent=4)
