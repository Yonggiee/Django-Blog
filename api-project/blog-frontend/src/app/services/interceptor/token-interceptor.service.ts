import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpHeaders, HttpErrorResponse, HttpEvent } from '@angular/common/http';
import { UserService } from '../user/user.service';
import { catchError, switchMap, filter, take } from 'rxjs/operators'
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor{
  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null)

  constructor(private userService: UserService) { }

  intercept(req, next) {
    if (req.method == "POST") {
      const accessToken = localStorage.getItem('accessToken');
      let httpOptionsWithToken =  new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
      });
      let tokenisedReq = req.clone({
        headers: httpOptionsWithToken
      })
      return next.handle(tokenisedReq).pipe(catchError(error => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          return this.handle401Error(req, next);
        }
      }));
    }
    return next.handle(req);
  }

  handle401Error(req, next) {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);
      return this.userService.refreshAccessToken().pipe(
        switchMap(() => {
          this.isRefreshing = false;
          this.refreshTokenSubject.next("token");
          return next.handle(this.addToken(req));
        }
      ));
    } else {
      return this.refreshTokenSubject.pipe(
        filter(token => token != null),
        take(1),
        switchMap(() => {
          return next.handle(this.addToken(req));
        })
      )
    }
  }

  private addToken(req) {
    const accessToken = localStorage.getItem('accessToken');
    let httpOptionsWithToken = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken
    });
    let tokenisedReq = req.clone({
      headers: httpOptionsWithToken
    })
    return tokenisedReq;
  }
}


     