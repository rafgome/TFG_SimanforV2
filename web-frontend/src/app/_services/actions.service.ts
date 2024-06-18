import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { ApiService } from "./api.service";
import { Actions } from "../_models/actions";
import { HttpHeaders } from "@angular/common/http";
import { ServerResponse } from "../_models/serverResponse";
import { AuthService } from "./auth.service";

@Injectable({ providedIn: "root" })
export class ActionService {
  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}

  _getHeaders(): HttpHeaders {
    const token = this.authService.getAuthToken();
    return new HttpHeaders({
      Authorization: token,
    });
  }

  _getJSONHeaders(): HttpHeaders {
    const token = this.authService.getAuthToken();
    return new HttpHeaders({
      Authorization: token,
      "Content-Type": "application/json",
    });
  }

  getActions(): Observable<ServerResponse> {
    return this.apiService.get("/actions", null, this._getHeaders());
  }

  addAction(actionData: Actions): Observable<ServerResponse> {
    return this.apiService.post("/actions", actionData, this._getJSONHeaders());
  }

  generateSmartelo(id: number): Observable<ServerResponse> {
    return this.apiService.postSmartelo(`/actions/${id}/generateSmartelo`, null, this._getHeaders());
  }

  deleteAction(id: number): Observable<ServerResponse> {
    return this.apiService.delete(`/actions/${id}`, this._getHeaders());
  }
}
