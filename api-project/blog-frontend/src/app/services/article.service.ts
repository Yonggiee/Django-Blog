import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {

  baseurl = "http://0.0.0.0:8000";
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'})

  constructor(private http: HttpClient) { }

  getAllArticles(): Observable<any>{
    return this.http.get(this.baseurl + '/articles/', {headers: this.httpHeaders});
  }

  getDetailedArticle(slug): Observable<any> {
    return this.http.get(this.baseurl + '/article/' + slug, { headers: this.httpHeaders });
  }

  getArticleComments(slug): Observable<any> {
    return this.http.get(this.baseurl + '/article/' + slug + '/comments/', { headers: this.httpHeaders });
  }

  postArticle(article): Observable<any> {
    const body = article
    return this.http.post(this.baseurl + '/articles/', body, { headers: this.httpHeaders });
  }
}
