### SQL Tool ver 1.0

此版本包含 SQL 工具的初始版本，設計用於執行和管理 MS SQL Server 和 Oracle 數據庫的 SQL 查詢。以下是此版本包含的功能和特性。

#### 功能：

1. **登入畫面**：
    - **伺服器類型選擇**：選擇 MS SQL Server 或 Oracle。
    - **登入資訊**：
        - 對於 MS SQL Server：Host、Database/Schema、Username、Password、Trust Server Certificate。
        - 對於 Oracle：Host、Port（預設 1521）、Service Name/SID、Username、Password。
    - **記住我**：保存登入資訊以供未來使用。
    - **動態表單更新**：根據所選伺服器類型更新表單字段。
    - **進度條**：顯示登入進度。
    - **錯誤處理**：顯示登入失敗的相應錯誤消息。

2. **主應用程式窗口**：
    - **執行 SQL 查詢**：打開窗口以輸入和執行自定義 SQL 查詢。
    - **功能 1**：
        - 打開一個窗口輸入 `Com ID` 和 `ERP ID`。
        - 查詢指定 `Com ID` 中提供的 `ERP ID` 的數據庫。
        - 以表格格式顯示結果。

3. **功能 1 詳細流程**：
    - **輸入 Com ID 和 ERP ID**：用戶輸入這些值以查詢數據庫。
    - **顯示結果**：以表格格式顯示查詢結果，具有自定義列標題（`ERP ID`、`Status`）。
    - **更改狀態**：
        - 提示用戶是否要更改所選記錄的狀態。
        - 如果選擇“是”，打開一個新窗口輸入新狀態（僅允許 '3'、'1'、'N'）。
        - 在更新數據庫之前確認用戶的狀態更改。
        - 使用新狀態更新查詢記錄的 `INAPOS` 列。

4. **窗口關閉處理**：
    - 確保在任何窗口通過後退按鈕或直接關閉時，SQL 連接將被關閉。

#### 代碼結構：

- **main.py**：包含主登入畫面和主應用邏輯。
- **oracle_screen.py**：包含 Oracle 數據庫主窗口的邏輯。
- **mssql_screen.py**：包含 MS SQL Server 主窗口的邏輯。
- **oracle_functions/function1.py**：包含功能 1 的邏輯。

#### 示例使用：

1. **登入**：
    - 選擇伺服器類型（MS SQL Server 或 Oracle）。
    - 輸入所需的登入資訊。
    - 點擊“登入”。

2. **執行 SQL 查詢**：
    - 點擊“執行 SQL 查詢”。
    - 輸入自定義 SQL 查詢。
    - 點擊“執行”以表格格式查看結果。

3. **功能 1**：
    - 點擊“功能 1”。
    - 輸入 `Com ID` 和 `ERP ID`。
    - 點擊“確認”。
    - 如果找到數據，將提示是否更改狀態。
    - 如果選擇“是”，輸入新狀態（'3'、'1'、'N'）。
    - 確認狀態更改。
    - 狀態將在數據庫中更新。

#### 安裝：

1. 克隆倉庫：
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. 安裝所需的套件：
    ```bash
    pip install -r requirements.txt
    ```

3. 安裝 Oracle 客戶端：
    - 下載 Oracle Instant Client：https://www.oracle.com/database/technologies/instant-client/downloads.html
    - 解壓縮下載的檔案到目錄，例如 `C:\oracle\instantclient_19_8`
    - 配置環境變量：
      - 將 Oracle Instant Client 目錄添加到 `PATH`：
        - Windows:
          1. 右鍵點擊“此電腦”或“我的電腦”，選擇“屬性”。
          2. 點擊“高級系統設置”。
          3. 點擊“環境變量”。
          4. 在“系統變量”下，找到 `Path`，選擇並點擊“編輯”。
          5. 點擊“新建”，輸入 Oracle Instant Client 的路徑（例如 `C:\oracle\instantclient_19_8`）。
          6. 點擊“確定”保存變更。

        - Linux / macOS:
          ```bash
          export LD_LIBRARY_PATH=/path/to/instantclient:$LD_LIBRARY_PATH
          export PATH=/path/to/instantclient:$PATH
          ```

4. 運行應用程式：
    ```bash
    python main.py
    ```

#### 依賴項：

- `tkinter`：用於 GUI 組件。
- `cx_Oracle`：用於 Oracle 數據庫連接。
- `pyodbc`：用於 MS SQL Server 數據庫連接。

#### 注意：

- 確保已正確安裝和配置 Oracle 客戶端以支持 `cx_Oracle`。
- 根據需要修改 `requirements.txt` 以包含任何其他依賴項。

此版本為執行和管理 SQL 查詢提供了直觀的 GUI 基礎，未來版本可以添加更多功能。如果遇到任何問題或有改進建議，請在 GitHub 上創建問題。

**Full Changelog**: https://github.com/yusyuan9224/SQL-TOOL/commits/work