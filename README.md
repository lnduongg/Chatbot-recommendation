![Packagist Dependency Version](https://img.shields.io/badge/python-3.11.6-blue?style=flat-square&logo=blue)
![Packagist Version](https://img.shields.io/badge/packagist-1.0-brightgreen?style=flat-square)
![Language Support](https://img.shields.io/badge/language-vietnamese-red?style=flat-square)

Chatbot AI
===
Đây là Chatbot AI có thể đưa ra gợi ý và khuyên nhủ về sản phẩm dựa trên bộ dữ liệu người dùng cung cấp cho nó.
## Chức năng
- Tự động sàng lọc ra những sản phẩm phù hợp với yêu cầu của người dùng.
- Đưa ra câu trả lời về các sản phẩm dựa trên yêu cầu của người dùng.

## Cài đặt môi trường
- [PostgreSQL](https://www.postgresql.org)
- [Python 3.11.6](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe)
- [Visual Studio Code](https://code.visualstudio.com/)
- Khởi động terminal và trỏ vào thư mục dự án: VD: d:/projects/hi1-chatbot.
- Chạy câu lệnh sau để cài đặt requirements:
  ```
  pip install -r requirements.txt
  ```

## Khởi tạo thông tin ban đầu cho AI
- Trong file **.env**:
  ```
  OPENAI_KEY = ""
  MODEL = ""
  ```
  Hãy điền thông tin tương ứng cho API key của bạn vào trong dấu **" "** của OPENAI_KEY và model của AI vào trong dấu **" "** của MODEL.

- Trong file **app/service/chatbot_service.py**, bạn tìm đoạn lệnh như sau:
  ```
  # Gemini
  llm = ChatGoogleGenerativeAI(model=settings.MODEL, google_api_key=settings.API_KEY)

  # OpenAI
  # llm = ChatOpenAI(model_name=settings.MODEL, openai_api_key=settings.API_KEY)
  ```
  Nếu bạn sử dụng Gemini, giữ nguyên phần này, nếu bạn sử dụng OpenAI hoặc các AI tương thích với client của OpenAI, thay đổi code phần này như sau:
  ```
  # Gemini
  # llm = ChatGoogleGenerativeAI(model=settings.MODEL, google_api_key=settings.API_KEY)

  # OpenAI
  llm = ChatOpenAI(model_name=settings.MODEL, openai_api_key=settings.API_KEY)
  ```
## Khởi tạo thông tin cho bộ dữ liệu
- Chỉnh sửa kết nối đến database của PostgreSQL trong file **.env**:
  ```
  DB_NAME=<tên database - mặc định là products>
  DB_USER=<tên user - mặc định là postgres>
  DB_PASSWORD=<mật khẩu - mặc định là r>
  DB_HOST=<host - mặc định là localhost>
  DB_PORT=<cổng kết nối - mặc định là 5432>
  TB_NAME=<tên bảng - mặc định là products>
  ```

- Trong trường hợp bạn chưa có database, bạn có thể khởi tạo database bằng cách:

  - Chỉnh **DB_NAME** theo tên database bạn muốn tạo.

  - Chỉnh **TB_NAME** theo tên table bạn muốn tạo.

  - Chỉnh sửa dữ liệu theo ý muốn trong file **app/db/model.py** hoặc để nguyên theo mẫu có sẵn ( gồm id, tên, danh mục, màu sắc và giá tiền ).
  
  - Thêm lệnh sau để khởi tạo database:
    ```
    python -m app.db.database_create
    ```
    Nếu kết quả báo thành công, bạn có thể vào kiểm tra trong PostgreSQL để kiểm tra nó đã tạo một database mới chưa.

  - Thêm lệnh sau để khởi tạo bộ tạo dữ liệu tự động (các lệnh này bạn chỉ cần làm một lần nếu đây là lần đầu tiên bạn sinh bộ tạo dữ liệu):
    ```
    alembic init alembic
    ```
  - Chương trình sẽ tạo ra file **alembic.ini** và folder **alembic**.
  - Bạn cần vào file **alembic.ini**, tìm dòng code sau:
    ```
    sqlalchemy.url = driver://user:pass@localhost/dbname
    ```
    và xoá nó đi.

  - Tiếp theo vào folder **alembic** và tìm file **env.py**, xoá toàn bộ code trong file đó và thay bằng code sau:
    ```
    import os
    from logging.config import fileConfig
    from sqlalchemy import engine_from_config, pool
    from alembic import context
    from app.core.config import settings
    from app.db.model import Base  
    config = context.config

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    target_metadata = Base.metadata

    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode."""
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online() -> None:
        """Run migrations in 'online' mode."""
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)

            with context.begin_transaction():
                context.run_migrations()

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()

    ```
    - Tiếp đó chạy dòng lệnh sau trong terminal:
    ```
    alembic revision --autogenerate -m "initial migration"
    ```

  - Chạy dòng lệnh sau để chương trình tự sinh một bảng đặt theo **TB_NAME** trong file .env của bạn
    ```
    alembic upgrade head
    ```
  - Tiếp theo nếu bạn muốn tự sinh một bộ dữ liệu ngẫu nhiên, bạn chạy dòng lệnh này trong terminal:
    ```
    python -m app.db.database_seeder
    ```
    ### <ins>**Lưu ý**</ins>: 
  - Ở đây là bộ sinh tự sinh dữ liệu đang theo các trường dữ liệu có sẵn, nếu **model.py** của bạn có khác so với mẫu có sẵn, hãy sửa nội dung trong file **app/db/database_seeder.py** cho phù hợp với yêu cầu của bạn.

  - Bạn có thể kiểm tra dữ liệu đã được sinh ra trong PostgreSQL bằng câu lệnh:
    ```sql
    SELECT * FROM public.<TB_NAME>
    ```

## Khởi chạy chương trình
- Đầu tiên ta cần khởi tạo kết nối đến FastAPI:
  ```
  uvicorn app.main:app --reload
  ```
- Sau đó chạy lệnh sau:

  ```
  python -m test_bot
  ```
- Nếu gọi đúng, chương trình sẽ hiển thị như sau:
  ```
  Nhập 'exit' để thoát
  Bạn:
  ```
  Nhập câu truy vấn của bạn, ví dụ:
  ```
  Nhập 'exit' để thoát
  Bạn: Tôi cần tìm hai sản phẩm là đồ chơi có tổng giá dưới 500
  ```
  Sau đó bot sẽ trả lời lại cho bạn ví dụ như:
  ```
  Kết quả tìm kiếm:
  ID    | Tên | Loại| Màu                           | Giá
  ------------------------------------------------------------
  16    | Even| Toys| ['PeachPuff', 'DarkViolet']   | 138.53
  26    | Tax | Toys| ['SlateBlue', 'Magenta']      | 117.14


  Bot: 1. Bộ xếp hình Lego (giá khoảng 250.000 VNĐ)
  2. Búp bê Barbie (giá khoảng 200.000 VNĐ)
  ```
  ### <ins>**Lưu ý**</ins>:
  - Ở đây bot in ra câu trả lời dựa trên các trường dữ liệu có sẵn, nếu bạn có thay đổi trong dữ liệu thì có thể sửa cách in ra ở file **app/service/chatbot_data.py** tại dòng 54:
    ```
    formatted_result = f"{'ID':<{id_width}} | {'Tên':<{name_width}} | {'Loại':<{type_width}} | {'Màu':<{color_width}} | {'Giá':<{price_width}}\n"
    ```
    và dòng 59:
    
    ```
    formatted_result += f"{row[0]:<{id_width}} | {row[1]:<{name_width}} | {row[2]:<{type_width}} | {str(row[3]):<{color_width}} | {row[4]:<{price_width}.2f}\n"
    ```