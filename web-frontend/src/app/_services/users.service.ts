import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { ApiService } from "./api.service";
import { CommonService } from "./common.service";
import { ServerResponse } from "./../_models/serverResponse";

import { HttpHeaders } from "@angular/common/http";
import { User } from "../_models/user";
import { AuthService } from "./auth.service";

@Injectable({ providedIn: "root" })
export class UsersService {
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

  getUsers(): Observable<ServerResponse> {
    return this.apiService.get("/user", null, this._getHeaders());
  }

  getRequestedUsers(): Observable<ServerResponse> {
    return this.apiService.get("/requested", null, this._getHeaders());
  }

  addUser(user: User): Observable<ServerResponse> {
    return this.apiService.postFormData(
      "/register",
      this.commonService.objectToFormData(user),
      this._getHeaders()
    );
  }

  deleteUser(id: number): Observable<ServerResponse> {
    return this.apiService.delete(`/user/${id}`, this._getHeaders());
  }

  updateUser(user: User): Observable<ServerResponse> {
    return this.apiService.postFormData(
      `/user/${user.id}`,
      this.commonService.objectToFormData(user),
      this._getHeaders()
    );
  }
}
