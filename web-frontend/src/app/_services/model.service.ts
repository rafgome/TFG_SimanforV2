import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { ApiService } from "./api.service";
import { CommonService } from "./common.service";
import { ServerResponse } from "./../_models/serverResponse";

import { HttpParams, HttpHeaders } from "@angular/common/http";
import { Model } from "../_models/model";
import { AuthService } from "./auth.service";

@Injectable({ providedIn: "root" })
export class ModelService {
  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private commonService: CommonService
  ) {}

  _getHeaders(): HttpHeaders {
    const token = this.authService.getAuthToken();
    return new HttpHeaders({
      Authorization: token,
    });
  }

  getModels(): Observable<ServerResponse> {
    return this.apiService.get("/model", null, this._getHeaders());
  }

  getCuttingModels(): Observable<ServerResponse> {
    const params = new HttpParams().append("type", "cutting");
    return this.apiService.get("/model", params, this._getHeaders());
  }

  getProjectionModels(): Observable<ServerResponse> {
    const params = new HttpParams().append("type", "projection");
    return this.apiService.get("/model", params, this._getHeaders());
  }

  addModel(model: Model): Observable<ServerResponse> {
    return this.apiService.postFormData(
      "/model",
      this.commonService.objectToFormData(model),
      this._getHeaders()
    );
  }

  deleteModel(id: string): Observable<ServerResponse> {
    return this.apiService.delete(`/model/${id}`, this._getHeaders());
  }

  editModel(model: Model): Observable<ServerResponse> {
    return this.apiService.postFormData(
      `/model/${model.id}`,
      this.commonService.objectToFormData(model),
      this._getHeaders()
    );
  }
}
