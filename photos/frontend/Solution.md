# Final Solution

After many attempts, it was finally decided to abandon the Websocket solution. The backend remained unchanged, and a group of file uploads were split into single files and uploaded sequentially on the frontend.

- src/app/app.component.html
  - Files Select Button
  - Upload Button
  - Upload Progress Info
- src/app/app.component.ts
  - onFilesSelected: select a group files
  - uploadFiles: upload a group of files
  - uploadFile: upload a single file

## Demo

**Frontend**

```
cd photos/frontend
npm install
npm start
```

**Backend**

```
cd photos
python upload_progress.py
```

