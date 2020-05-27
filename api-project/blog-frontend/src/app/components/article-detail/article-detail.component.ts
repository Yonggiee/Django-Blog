import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ArticleService } from 'src/app/services/article.service';

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.component.html',
  styleUrls: ['./article-detail.component.css']
})
export class ArticleDetailComponent implements OnInit {

  id;
  article;

  constructor(private route: ActivatedRoute, 
    private articleService: ArticleService) { }

  ngOnInit(): void {
    this.getIdFromParams();
    this.getDetailedArticle();
  }

  getIdFromParams() {
    this.route.paramMap.subscribe(params => {
      this.id = params.get('id')
    })
  }

  getDetailedArticle() {
    this.articleService.getDetailedArticle(this.id).subscribe(
      article => {
        this.article = article;
      }
    )
  }
}
