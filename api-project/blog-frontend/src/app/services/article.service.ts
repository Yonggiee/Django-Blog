import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ArticleService {
  baseurl = 'http://0.0.0.0:8000';
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  };

  constructor(private http: HttpClient) {}

  getAllArticles(): Observable<any> {
    return this.http.get(this.baseurl + '/articles/', this.httpOptions);
  }

  getDetailedArticle(slug): Observable<any> {
    return this.http.get(this.baseurl + '/article/' + slug, this.httpOptions);
  }

  getArticleComments(slug): Observable<any> {
    return this.http.get(this.baseurl + '/article/' + slug + '/comments/', this.httpOptions);
  }

  postArticle(article): Observable<any> {
    const body = article;
    return this.http.post(this.baseurl + '/articles/', body, this.httpOptions);
  }
}
