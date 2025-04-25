# MBTA-Web-App-Project
This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.

## Project Writeup and Reflection:
Team Members: Aryan Shanker and Joshua Bell. 

## Project Overview
Writing

# MBTA Web App Project

**Team Members:**  
- Joshua Bell  
- Aryan Shanker

---

## 1. Project Overview

Our MBTA Web App allows users to enter a location (e.g., "Fenway Park") and receive the name of the nearest MBTA stop along with its wheelchair accessibility status. This project integrates real-time geolocation and transit data from two external APIs—Mapbox and MBTA Realtime. The backend handles API interactions and geocoding logic, while the frontend provides an intuitive user interface through a Flask web application. Users can enter a place name, submit the form, and see the results dynamically rendered on a new page. Our application emphasizes modular design, clean routing, and simplicity for the end user.

---

## 2. Reflection

**Development Process**  
We divided the work by function. Aryan focused on the backend logic in `mbta_helper.py`, which included working with the Mapbox Geocoding API to convert place names to coordinates, and using the MBTA Realtime API to retrieve the nearest transit stop. I (Joshua) handled the Flask web application (Part 2), setting up routing, rendering templates, and processing form data submitted by users. One of the biggest challenges was aligning the inputs and outputs of the backend functions with the frontend expectations, particularly in ensuring error handling worked smoothly when users entered invalid locations. Once routing and template logic were in place, the app started working as expected.

**Team Collaboration**  
Our team collaboration was smooth. We each worked on separate files and integrated our code once both parts were functional. GitHub made version control and syncing easier, and we communicated clearly about function interfaces so we could build independently but align at the integration phase. While our individual contributions were separate, we reviewed each other’s work to ensure the whole project ran seamlessly. If we did the project again, we would have scheduled a mid-way sync meeting to test integration earlier and troubleshoot any mismatches sooner.

**Learning Experience & AI Tools**  
I (Joshua) learned a lot about how web forms work, how POST requests are handled in Flask, and how to route users to new views with dynamic content. Aryan gained experience working with web APIs and handling structured JSON data in Python. We both benefited from using AI tools like ChatGPT to help write and debug Python and HTML code, troubleshoot API issues, and clarify Flask's routing behavior. AI tools made it easier to move quickly and debug without getting stuck. If we had known earlier how useful tools like Flask’s debug mode and `pprint` are, we could have saved time during testing. Overall, we’re leaving this project with stronger backend + frontend dev skills and the confidence to build future apps from scratch.

---

### 🔽 Screenshots

1. **Home Page (Form Input):**  
   ![Home Page Screenshot](58f95199-6cec-4d44-8b55-54855cd576ed.png)

2. **Result Page (Nearest MBTA Stop):**  
   ![Result Screenshot](0831ecb4-edd3-4809-9903-77c03dc2adde.png)

3. **Error Page (Invalid Input):**  
   ![Error Screenshot](6522180c-5c7b-43ab-9cf8-3360a3bafac7.png)

---

