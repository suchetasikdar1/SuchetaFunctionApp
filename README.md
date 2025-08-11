SuchetaFunctionApp is an Azure Function App built with Python 3.10. It is activated via an HTTP trigger. It allows users to select a Canadian animal from a dropdown menu and returns the name of Canadian National Park(s) where that animal can be found.

Note: This app only works with Python 3.10. Higher versions (e.g., 3.11 or 3.12) are not supported by the Azure Functions runtime and may cause deployment errors.
Folder structure matters Ensure your project follows the correct Azure Functions layout when deploying via VS Code or CLI
Do not allow public access to the associated Azure Storage Account. Instead:
Use Virtual Network Integration for your Function App.
Create a Private Endpoint for the Storage Account.
Configure a Private DNS Zone to resolve storage URLs securely.
Ensure the VNet links are properly configured between:
- The Function App’s subnet.
- The Private Endpoint’s subnet.
- The Private DNS Zone.
This setup ensures that all traffic between your Function App and Storage Account stays within your private network, improving security.

Link to the Function App: https://suchetafunctionapp-dbchehfzdcb8fwf0.canadaeast-01.azurewebsites.net/api/MyFunction

Have fun coding! This is for educational purposes only.
