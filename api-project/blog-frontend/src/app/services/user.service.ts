import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { baseurl, httpOptions } from './commons.service';
import { LoginNotiService } from './login-noti.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  errors: any = [];

  constructor(
    private http: HttpClient,
    private loginNotiService: LoginNotiService
  ) {}

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user) {
    this.http
      .post(baseurl + '/api/token/', user, httpOptions)
      .subscribe(
        (data) => {
          this.updateAfterLogin(data);
          this.loginNotiService.triggerService();
        },
        (err) => {
          this.errors = err['error'];
        }
      );
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    this.http
      .post(
        baseurl + 'api/token/refresh/',
        JSON.stringify({ token: refreshToken }),
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
    localStorage.clear();
    this.loginNotiService.triggerService();
  }

  public requireReaccessToken() {
    const dateNow = Date.now();
    // return dateNow > this.accessTokenExpires;
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
    localStorage.setItem('accessToken', token);
    this.errors = [];
    const token_decoded = this.decodeToken(token)
    const accessTokenExpires = token_decoded.exp * 1000;
    localStorage.setItem('accessTokenExpires', accessTokenExpires.toString());
  }

  private updateRefresh(token){
    localStorage.setItem('refreshToken', token);
    this.errors = [];
    const token_decoded = this.decodeToken(token)
    const refreshTokenExpires = token_decoded.exp * 1000;
    localStorage.setItem('refreshTokenExpires', refreshTokenExpires.toString());
  }

  private decodeToken(token) {
    const token_parts = token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    return token_decoded;
  }
}
