import {
  Output,
  EventEmitter,
  ChangeDetectorRef,
  Component
} from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { HttpClient, HttpRequest, HttpEventType, HttpErrorResponse } from '@angular/common/http';

import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators'
import { UploadProgress, initialUploadProgress } from './upload/models/upload-progress.interface';
import { UploadService } from './upload/services/upload.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'frontend';
  files: File[] = [];
  metafeatures: string[] = [];
  uploadForm: FormGroup = this.fb.group({
    upload: [null],
    comment: [null]
  });
  uploadProgress: UploadProgress = initialUploadProgress;
  hasActiveProgress$ = new Subject<boolean>();
  metafeaturesSet$ = new Subject<void>();

  totalFiles = 0;
  currentFileIndex = 0;
  currentFileProgress  = 0;
  currentFilename = '';
  uploadInProgress = false;

  isLoadingBar = false;

  constructor(
    private fb: FormBuilder,
    private cr: ChangeDetectorRef,
    private upload: UploadService,
    private http: HttpClient
  ) {}

  onFilesSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    for (let i = 0; i < (target.files ? target.files.length: 0); i++) {
      target.files && this.files.push(target.files[i]);
    }
    this.totalFiles = this.files.length;
  }

  uploadFiles() {
    console.log("-->uploadFiles");
    const wSName = this.getWSName(this.files);
    const { upload, comment, ...metafeatures } = this.uploadForm.value;
    this.hasActiveProgress$.next(true);
    this.isLoadingBar = true;

  
    // Use this for uploading files one by one
    this.upload
      .uploadFiles(this.files)
      .pipe(takeUntil(this.hasActiveProgress$))
      .subscribe({
        next: uploadProgress_ => this.refreshProgress(uploadProgress_),
        complete: () => this.onFinishedUpload(comment, wSName, { ...metafeatures })
      });

    this.cr.detectChanges();

  }

  getWSName(files: File[]) {
    return this.upload.getWSName(files[0]) ?? '';
  }

  private onFinishedUpload(comment: any, wSName: string, metafeatures: any) {
    if (comment) {
      this.upload.updateComment(wSName, comment).pipe(take(1)).subscribe();
    }

    this.sendMetafeatures(wSName, metafeatures);
  }

  private refreshProgress(uploadProgress: UploadProgress) {
    console.log("refreshProgress:", uploadProgress);
    this.uploadProgress = uploadProgress;
    this.cr.detectChanges();
  }

  private sendMetafeatures(wSName: string, metafeatures: any) {
    this.upload
      .setMetafeatures(wSName, metafeatures)
      .pipe(takeUntil(this.metafeaturesSet$))
      .subscribe({
        complete: () => this.finishUpload()
      });
  }

  private finishUpload() {
    this.metafeaturesSet$.next();
    this.uploadForm.reset();
    this.uploadProgress = initialUploadProgress;
    this.hasActiveProgress$.next(false);
    this.isLoadingBar = false;
  }

  onUploadCancel() {
    this.uploadProgress = initialUploadProgress;
    this.hasActiveProgress$.next(false);
  }

  async uploadFiles1() {
    this.uploadInProgress = true;

    this.currentFileProgress = 0;
    for (let i = 0; i < this.files.length; i++) {
      this.currentFileIndex = i;
      this.currentFilename = this.files[i].name;
      console.log(this.files[i].webkitRelativePath);

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
