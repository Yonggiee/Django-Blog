import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Observable } from 'rxjs';
import { httpOptions, baseurl } from './commons.service';

@Injectable({
  providedIn: 'root',
})
export class ArticleService {

  constructor(private http: HttpClient) {}

  getAllArticles(): Observable<any> {
    return this.http.get(baseurl + '/articles/', httpOptions);
  }

  getDetailedArticle(slug): Observable<any> {
    return this.http.get(baseurl + '/article/' + slug, httpOptions);
  }

  getArticleComments(slug): Observable<any> {
    return this.http.get(baseurl + '/article/' + slug + '/comments/', httpOptions);
  }

  postArticle(article): Observable<any> {
    const body = article;
    const accessToken = localStorage.getItem('accessToken');
    let httpOptionsWithToken = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken
      })
    };
    return this.http.post(baseurl + '/articles/', body, httpOptionsWithToken);
  }
}
