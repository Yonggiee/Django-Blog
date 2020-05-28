import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { baseurl, httpOptions } from './commons.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  accessToken: string;
  accessTokenExpires: Date;
  refreshToken: string;
  refreshTokenExpires: Date;
  errors: any = [];

  constructor(private http: HttpClient) {}

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user) {
    this.http
      .post(baseurl + '/api/token/', user, httpOptions)
      .subscribe(
        (data) => {
          this.updateAfterLogin(data);
        },
        (err) => {
          this.errors = err['error'];
        }
      );
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshAccessToken() {
    this.http
      .post(
        baseurl + 'api/token/refresh/',
        JSON.stringify({ token: this.refreshToken }),
        httpOptions
      )
      .subscribe(
        (data) => {
          this.updateAfterRefreshAccessToken(data);
        },
        (err) => {
          this.errors = err['error'];
        }
      );
  }

  public logout() {
    this.accessToken = null;
    this.refreshToken = null;
    this.accessTokenExpires = null;
    this.refreshTokenExpires = null;
  }

  private updateAfterLogin(data) {
    const accessToken = data['access'];
    const refreshToken = data['refresh'];
    this.updateAccess(accessToken);
    this.updateRefresh(refreshToken);
  }

  private updateAfterRefreshAccessToken(data){
    const accessToken = data['access'];
    this.updateAccess(accessToken);
  }

  private updateAccess(token){
    this.accessToken = token;
    this.errors = [];
    const token_decoded = this.decodeToken(token)
    this.accessTokenExpires = new Date(token_decoded.exp * 1000);
  }

  private updateRefresh(token){
    this.refreshToken = token;
    this.errors = [];
    const token_decoded = this.decodeToken(token)
    this.refreshTokenExpires = new Date(token_decoded.exp * 1000);
  }

  private decodeToken(token) {
    const token_parts = token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    return token_decoded;
  }
}
