import { Injectable } from "@angular/core";
import { environment } from "../../environments/environment";
import { HttpClient, HttpParams, HttpHeaders } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";

@Injectable()
export class ApiService {
  headers = {
    "Content-Type": "application/json",
  };

  constructor(private http: HttpClient) {}

  private formatErrors(error: any) {
    return throwError(error);
  }

  get(
    path: string,
    params: HttpParams = new HttpParams(),
    header: HttpHeaders = new HttpHeaders(this.headers),
    responseType: string = "json"
  ): Observable<any> {
    return this.http
      .get(`${environment.api_url}${path}`, {
        headers: header,
        params: params,
        responseType: responseType as "text",
      })
      .pipe(catchError(this.formatErrors));
  }

  getFromJson(path: string): any {
    return this.http.get(path).pipe(catchError(this.formatErrors));
  }

  put(
    path: string,
    body: Object = {},
    header: HttpHeaders = new HttpHeaders(this.headers)
  ): Observable<any> {
    return this.http
      .put(`${environment.api_url}${path}`, JSON.stringify(body), {
        headers: header,
      })
      .pipe(catchError(this.formatErrors));
  }

  post(
    path: string,
    body: Object = {},
    header: HttpHeaders = new HttpHeaders(this.headers)
  ): Observable<any> {
    return this.http
      .post(`${environment.api_url}${path}`, JSON.stringify(body), {
        headers: header,
      })
      .pipe(catchError(this.formatErrors));
  }

  postSmartelo(path: string, body: Object = {}, header: HttpHeaders = new HttpHeaders(this.headers)): Observable<any> {
    return this.http.post(`${environment.api_url}${path}`, JSON.stringify(body), {headers: header, responseType: 'blob'})
      .pipe(catchError(this.formatErrors));
  }

  postFormData(
    path: string,
    body: FormData,
    header: HttpHeaders = new HttpHeaders()
  ): Observable<any> {
    return this.http
      .post(`${environment.api_url}${path}`, body, { headers: header })
      .pipe(catchError(this.formatErrors));
  }

  delete(
    path: string,
    header: HttpHeaders = new HttpHeaders(this.headers)
  ): Observable<any> {
    return this.http
      .delete(`${environment.api_url}${path}`, { headers: header })
      .pipe(catchError(this.formatErrors));
  }
}
