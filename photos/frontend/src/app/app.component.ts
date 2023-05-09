import { Component } from '@angular/core';
import { HttpClient, HttpRequest, HttpEventType, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'frontend';
  files: File[] = [];
  totalFiles = 0;
  currentFileIndex = 0;
  currentFileProgress  = 0;
  currentFilename = '';
  uploadInProgress = false;

  constructor(private http: HttpClient) {}

  onFilesSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    for (let i = 0; i < (target.files ? target.files.length: 0); i++) {
      target.files && this.files.push(target.files[i]);
    }
    this.totalFiles = this.files.length;
  }

  async uploadFiles() {
    this.uploadInProgress = true;

    this.currentFileProgress = 0;
    for (let i = 0; i < this.files.length; i++) {
      this.currentFileIndex = i;
      this.currentFilename = this.files[i].name;

      await this.uploadFile(this.files[i]);

      this.currentFileProgress = (this.currentFileIndex + 1) / this.totalFiles * 100;
    }

    this.uploadInProgress = false;
  }

  uploadFile(file: File): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      const formData = new FormData();
      formData.append('photos', file, file.name);

      const req = new HttpRequest('POST', '/api/upload', formData, {
        reportProgress: true
      });

      this.http.request(req).subscribe(
        event => {
          if (event.type === HttpEventType.Response) {
            resolve();
          }
        },
        err => {
          console.error('Upload error:', err);
          reject(err);
        }
      );
    });
  }
}
