# Tap Tracker

Tap Tracker é um sistema projetado para monitorar e rastrear interações de teclado e mouse em tempo real. ✨ A versão atual do cliente (v1.0) coleta dados de interação e os envia para um servidor centralizado, que será responsável por armazenar, processar e exibir relatórios detalhados.

## ⚙️ Estrutura do Projeto

### Cliente (Client)
- **🌐 Versão Atual**: 1.0
- **🔎 Funções**:
  - Monitoramento de eventos de teclado e mouse.
  - Envio de dados para o servidor por meio de uma REST API.
  - Configuração simples indicando o IP/DNS do servidor.

### Servidor (Server)f
- **🔄 Planejamento Atual**:
  - Receber e armazenar os dados enviados pelo cliente.
  - Gerar relatórios, gráficos e alertas.
  - Utilizar autenticação para controlar o acesso aos dados.
  - Banco de dados embutido (.db) gerado pelo próprio código.
  - Inicialmente hospedado on-premise.
  - Tabela `Users` para controle de acesso aos relatórios e dados coletados.

## ⚛️ Tecnologias Utilizadas
- **Cliente**:
  - Python

- **Servidor (planejado)**:
  - Linguagem: Python
  - Banco de Dados: Arquivo SQLite (.db)
  - API: RESTful

## 🗃️ Como Usar

### Cliente
1. Clone o repositório do Tap Tracker:
   ```bash
   git clone https://github.com/rockadu/tap-tracker.git
   ```
2. Configure o arquivo de configuração para apontar para o IP/DNS do servidor.
3. Execute o cliente:
   ```bash
   python client.py
   ```

### Servidor (Planejado)
O servidor será responsável por:
1. Armazenar dados enviados pelo cliente.
2. Processar e gerar relatórios e alertas.
3. Oferecer acesso seguro por meio de autenticação.

Instruções detalhadas para o servidor serão adicionadas futuramente.

## 🔄 Funcionalidades Principais
1. **⏳ Monitoramento em Tempo Real**:
   - Capacidade de capturar eventos de teclado e mouse com alta precisão.

2. **🌐 Comunicação Cliente-Servidor**:
   - O cliente envia pacotes de dados para o servidor configurado via API REST.

3. **📊 Análise de Dados (Planejado)**:
   - Relatórios detalhados e gráficos para visualização de padrões de interação.

4. **⚠️ Alertas (Planejado)**:
   - Geração de alertas automáticos com base em condições definidas pelo usuário.

## 📑 Estrutura do Banco de Dados
- **Tabela `Users`**:
  - Controla quem pode acessar os relatórios e dados coletados.
  - Não é utilizada para controlar quem pode enviar dados.

## 🌟 Contribuições
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do repositório.
2. Crie uma nova branch para sua funcionalidade ou correção.
3. Envie um pull request com uma descrição detalhada das alterações.

## 🔒 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com dedicação para facilitar a análise de interações humanas com dispositivos computacionais. 🚀

---

# Tap Tracker (English Version)

Tap Tracker is a system designed to monitor and track keyboard and mouse interactions in real-time. ✨ The current client version (v1.0) collects interaction data and sends it to a centralized server, which will store, process, and display detailed reports.

## ⚙️ Project Structure

### Client
- **🌐 Current Version**: 1.0
- **🔎 Features**:
  - Monitoring keyboard and mouse events.
  - Sending data to the server via a REST API.
  - Simple configuration specifying the server's IP/DNS.

### Server
- **🔄 Current Plan**:
  - Receive and store data sent by the client.
  - Generate reports, charts, and alerts.
  - Use authentication to control data access.
  - Embedded database (.db) created by the code.
  - Initially hosted on-premise.
  - `Users` table to control access to reports and collected data.

## ⚛️ Technologies Used
- **Client**:
  - Python

- **Server (planned)**:
  - Language: Python
  - Database: SQLite file (.db)
  - API: RESTful

## 🗃️ How to Use

### Client
1. Clone the Tap Tracker repository:
   ```bash
   git clone https://github.com/rockadu/tap-tracker.git
   ```
2. Configure the settings file to point to the server's IP/DNS.
3. Run the client:
   ```bash
   python client.py
   ```

### Server (Planned)
The server will:
1. Store data sent by the client.
2. Process and generate reports and alerts.
3. Provide secure access through authentication.

Detailed server instructions will be added in the future.

## 🔄 Main Features
1. **⏳ Real-Time Monitoring**:
   - Capture keyboard and mouse events with high accuracy.

2. **🌐 Client-Server Communication**:
   - The client sends data packets to the configured server via a REST API.

3. **📊 Data Analysis (Planned)**:
   - Detailed reports and charts to visualize interaction patterns.

4. **⚠️ Alerts (Planned)**:
   - Generate automatic alerts based on user-defined conditions.

## 📑 Database Structure
- **`Users` Table**:
  - Controls who can access reports and collected data.
  - Does not control who can send data.

## 🌟 Contributions
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed description of the changes.

## 🔒 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed with dedication to simplify human interaction analysis with computing devices. 🚀

