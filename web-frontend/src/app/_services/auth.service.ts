import { Injectable } from "@angular/core";
import { JwtHelperService } from "@auth0/angular-jwt";

@Injectable({ providedIn: "root" })
export class AuthService {
  private authToken = null;
  private role = null;

  constructor(public jwtHelper: JwtHelperService) {}

  public isAuthenticated(): boolean {
    const token = localStorage.getItem("authToken"); // Check whether the token is expired and return
    return !this.jwtHelper.isTokenExpired(token);
  }

  getAuthToken(): string {
    if (!!localStorage.getItem("authToken")) {
      this.authToken = localStorage.getItem("authToken");
    }

    return this.authToken;
  }

  setAuthToken(token: string) {
    this.authToken = token;
    localStorage.setItem("authToken", token);
  }

  public getRole(): string {
    if (!!localStorage.getItem("role")) {
      this.role = localStorage.getItem("role");
    }
    return this.role;
  }
  
  setRole(role: string) {
    this.role = role;
    localStorage.setItem("role", role);
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem("authToken");
    localStorage.removeItem("role");
  }
}
