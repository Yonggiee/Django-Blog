import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { baseurl, httpOptions } from '../commons.service';
import { LoginNotiService } from '../login-noti/login-noti.service';
import { map } from 'rxjs/operators';

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
    return this.http
      .post(
        baseurl + 'api/token/refresh/',
        JSON.stringify({ token: refreshToken }),
        httpOptions
      ).pipe(map((data) => {
        console.log("yes")
        console.log(data);
        this.updateAfterRefreshAccessToken(data);
      }))
  }

  public logout() {
    localStorage.clear();
    this.loginNotiService.triggerService();
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
  }

  private updateRefresh(token){
    localStorage.setItem('refreshToken', token);
    this.errors = [];
  }

}
