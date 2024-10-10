# Zoo Management API

## Overview

The Zoo Management API allows you to manage animals, employees, feeding schedules, and generate reports in the zoo.

### Base URL

`https://www.postman.com/technical-participant-73583793/zoo/documentation/hcywjhz/zoo-management-api`

### Authentication

None required.

---

## Endpoints

### Animals

#### Add an Animal

- **URL**: `/animals`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "species": "Elephant",
    "age": 10,
    "gender": "Female",
    "special_requirements": "Water nearby"
  }
  ```
