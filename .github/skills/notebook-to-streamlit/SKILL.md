---
name: notebook-to-streamlit
description: Convert the Rosa's Pizza notebook analysis into a Streamlit app while preserving the notebook's delivery simulation, cost calculations, and best-promise logic. Use when creating or updating the Streamlit app for this project.
---

# Convert the Notebook to a Streamlit App

Read the completed assignment notebook before writing the app. Reuse its constants, simulator, and calculation functions instead of inventing new business logic.

## Required app features

Create a Streamlit app that allows the user to:

1. Select a delivery zone from a dropdown menu.
2. Select a time block from a dropdown menu.
3. Set the minimum and maximum promised delivery times to test.
4. Adjust the profit margin per order.
5. Adjust the estimated churn per late order.
6. Adjust the refund cost per late order.
7. Click a button to calculate the best promised delivery time.
8. View the recommended promise and its net profit.

## Calculation requirements

- Test promises in 5-minute steps.
- Calculate the late-order cost using the notebook's cost logic.
- Calculate net profit for each candidate promise.
- Select the promise with the highest net profit.
- Use a fixed random seed so results are reproducible.
- Preserve the zone and time-block names used in the notebook.

## Project requirements

- Put the Streamlit interface in `app.py`.
- Put required Python packages in `requirements.txt`.
- Keep the code clear and suitable for deployment to Streamlit Community Cloud.
- Test the app locally before deployment.