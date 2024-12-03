# AI Agent-Based Marketing Analysis System

This system is designed to analyze e-commerce marketing data, focusing on improving cost efficiency, optimizing ROI, identifying wastage, and suggesting scaling strategies. It employs OpenAI's **Firecrawl** and **Swarm** frameworks to create and deploy specialized agents, each with a defined role in the analysis process.

---

## Features

- Analyze cost-effectiveness of traffic sources and campaigns.
- Optimize ROI by identifying underperforming campaigns.
- Highlight wastage in campaigns with high spending but low conversions.
- Suggest scaling opportunities for profitable campaigns.

---

## Agents and Their Roles

### **1. Cost Analyst Agent**
- **Description:** 
  Analyzes cost-effectiveness across traffic sources and campaigns by calculating metrics like cost-per-transaction and revenue-per-spend.
- **Key Methodology:**
  - Computes:
    - `cost_per_transaction` = `ad spend` ÷ (`transactions` + 1)
    - `revenue_per_spend` = `revenue` ÷ (`ad spend` + 1)
  - Aggregates and sorts the data by traffic source to identify high-performing campaigns.
- **Purpose:** Helps identify which traffic sources provide the best return on marketing investment.

### **2. ROI Optimizer Agent**
- **Description:** 
  Calculates ROI (Return on Investment) per campaign and flags campaigns that underperform.
- **Key Methodology:**
  - Computes:
    - `roi` = `revenue` ÷ (`ad spend` + 1)
  - Identifies campaigns where `roi` < 1 as underperforming.
- **Purpose:** Guides decisions on reallocating resources to improve campaign performance.

### **3. Wastage Analyst Agent**
- **Description:** 
  Identifies campaigns with high ad spend but low transaction volume, highlighting inefficient spending.
- **Key Methodology:**
  - Filters campaigns where:
    - `ad spend` > 1000
    - `transactions` < 10
- **Purpose:** Highlights wasted resources to ensure marketing spend is used effectively.

### **4. Scaling Strategist Agent**
- **Description:** 
  Suggests profitable campaigns, sources, or devices for scaling based on high ROI.
- **Key Methodology:**
  - Filters campaigns where:
    - `roi` > 3
- **Purpose:** Recommends successful campaigns that can be scaled to increase profitability.

---

## Analyzing Methodology

### **1. Data Preprocessing**
The dataset is loaded into a Pandas DataFrame and cleaned:
- Converts `date` into `datetime` format.
- Extracts new columns for `month`, `day`, and `weekday`.
- Removes currency symbols (`₱`) and commas from `ad spend` and `revenue` columns, converting them to integers.

### **2. Functions for Analysis**
Each agent uses a dedicated function to perform its task:
- **`analyze_cost_effectiveness`**: Aggregates data by `source` to compute cost-per-transaction and revenue-per-spend.
- **`optimize_roi`**: Identifies campaigns with ROI < 1.
- **`flag_wastage`**: Flags campaigns with high ad spend and low transactions.
- **`suggest_scaling`**: Identifies campaigns with ROI > 3.

---
# Set-Up Instructions

Follow these steps to set up and run the AI Agent-Based Marketing Analysis System.

## Step 1: Install Required Libraries

Make sure you have Python installed on your system, and then run the following command to install the necessary libraries:

```bash
pip install pandas numpy firecrawl swarm openai
```

### **Step 2: Obtain and Configure OpenAI API Key**

Obtain your API key from the OpenAI API.
Replace "YOUR_API_KEY_HERE" in the script with your actual API key:

```bash
api = OpenAI(api_key="YOUR_API_KEY_HERE")
```
### **Step 3: Load the Dataset**

Ensure the dataset is accessible, either from a public URL or locally. By default, the script uses a dataset hosted online:

```bash
data = pd.read_csv('https://path/to/your/dataset.csv')
```
If using a local dataset, update the path accordingly:

```bash
data = pd.read_csv('path/to/your/local_dataset.csv')
```
### **Step 4: Run the Agents**

Each agent is designed to perform a specific analysis task. Run the script to execute all agents:

```bash
python your_script.py
```

The following agents will be executed:

-Cost Analyst Agent: Evaluates cost-effectiveness.
-ROI Optimizer Agent: Identifies underperforming campaigns.
-Wastage Analyst Agent: Highlights inefficient campaigns.
-Scaling Strategist Agent: Suggests campaigns to scale up profitably.

### **Step 5: View Results**

The output from each agent will be printed to the console. For example:


Cost Analysis Results:
<Summary of cost-effectiveness per source>

ROI Optimizer Results:
<Summary of campaigns with low ROI>

Wastage Results:
<Summary of campaigns with high wastage>

Scaling Strategist Results:
<Summary of campaigns for scaling>
You can analyze these outputs to make informed marketing decisions.

