import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { ApiService } from "./api.service";
import { Scenario } from "./../_models/scenario";
import { CommonService } from "./common.service";
import { HttpHeaders } from "@angular/common/http";
import { ServerResponse } from "../_models/serverResponse";
import { AuthService } from "./auth.service";

@Injectable({ providedIn: "root" })
export class ScenarioService {
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

  getScenarios(): Observable<ServerResponse> {
    return this.apiService.get("/scenario", null, this._getHeaders());
  }

  addScenario(scenarioData: Scenario): Observable<ServerResponse> {
    return this.apiService.postFormData(
      "/scenario",
      this.commonService.objectToFormData(scenarioData),
      this._getHeaders()
    );
  }

  deleteScenario(id: number): Observable<ServerResponse> {
    return this.apiService.delete(`/scenario/${id}`, this._getHeaders());
  }

  runScenario(id: number): Observable<ServerResponse> {
    return this.apiService.post(
      `/scenario/${id}/start/`,
      {},
      this._getHeaders()
    );
  }

  downloadResult(id: number): Observable<ServerResponse> {
    return this.apiService.get(
      `/scenario/${id}/result/`,
      null,
      this._getHeaders(),
      "blob"
    );
  }
}
