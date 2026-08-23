# Steps to Create Prefect Cloud Account and API

Learn how to create a Prefect Cloud account and generate an API key for your project setup.

## Table of Contents

* [Create an Account and Workspace](#1-create-an-account-and-workspace)
* [Access the Profile Page](#2-access-the-profile-page)
* [Create the API Key](#3-create-the-api-key)
* [Credentials Needed](#4-credentials-needed)

## 1. Create an Account and Workspace

1. Visit [Prefect](https://app.prefect.cloud/auth/login) and create an account.
2. Once the account is created, proceed to create a workspace.
   
   ![Step 1 Screenshot](/image/prefect/prefectsetup1.png)

## 2. Access the Profile Page

1. Click on the user icon at the bottom left of the screen and select the options icon.
   
   ![Step 2 Screenshot](/image/prefect/prefectsetup2.png)
   
2. Find and note your profile handle.
   
   ![Step 2 Screenshot](/image/prefect/prefectsetup3.png)

## 3. Create the API Key

1. In the left menu, select the **API Keys** tab.
   
   ![Step 3 Screenshot](/image/prefect/prefectsetup4.png)

2. Click on **Create API Key** and provide a name for the key.
   
   ![Step 3 Screenshot](/image/prefect/prefectsetup5.png)

3. Click the **Create** button.
   
   ![Step 3 Screenshot](/image/prefect/prefectsetup6.png)

4. Copy the generated API key.

## 4. Copy Account ID and Workspace ID

Copy the account ID from the URL after the "account/" and the workspace ID from the URL after "workspace/".

   ![Step 4 Screenshot](/image/prefect/prefectsetup7.png)

## Credentials Needed

Make sure to input the following credentials into your project's clone directory [`.env`](/.env) file:

1. `Prefect_handle`: The profile handle from Step 2.
2. `Prefect_name`: The name of the workspace created in Step 1.
3. `Prefect_API_KEY`: The API key generated in Step 3.
4. `Prefect_Workspaceid`: The workspace ID from Step 4.
5. `Prefect_Accountid`: The account ID from Step 4.

