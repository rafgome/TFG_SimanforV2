import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { ApiService } from "./api.service";
import { Inventory } from "./../_models/inventory";
import { CommonService } from "./common.service";
import { HttpHeaders, HttpParams } from "@angular/common/http";
import { ServerResponse } from "../_models/serverResponse";
import { AuthService } from "./auth.service";

@Injectable({ providedIn: "root" })
export class InventoryService {
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

  getInventories(): Observable<ServerResponse> {
    return this.apiService.get("/inventory", null, this._getHeaders());
  }

  getSmarteloInventories(): Observable<ServerResponse> {
    const params = new HttpParams().append("smartelo", "true");
    return this.apiService.get("/inventory", params, this._getHeaders());
  }

  addInventory(inventoryData: Inventory): Observable<ServerResponse> {
    return this.apiService.postFormData(
      "/inventory",
      this.commonService.objectToFormData(inventoryData),
      this._getHeaders()
    );
  }

  deleteInventory(id: number): Observable<ServerResponse> {
    return this.apiService.delete(`/inventory/${id}`, this._getHeaders());
  }

  editInventory(inventoryData: Inventory): Observable<ServerResponse> {
    return this.apiService.postFormData(
      `/inventory/${inventoryData.id}`,
      this.commonService.objectToFormData(inventoryData),
      this._getHeaders()
    );
  }
}
