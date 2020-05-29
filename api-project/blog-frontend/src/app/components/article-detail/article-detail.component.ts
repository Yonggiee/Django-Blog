import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ArticleService } from 'src/app/services/article/article.service';

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.component.html',
  styleUrls: ['./article-detail.component.css']
})
export class ArticleDetailComponent implements OnInit {

  slug;
  article;
  comments;

  constructor(private route: ActivatedRoute, 
    private articleService: ArticleService) { }

  ngOnInit(): void {
    this.getSlugFromParams();
    this.getDetailedArticle();
    this.getComments();
  }

  getSlugFromParams() {
    this.route.paramMap.subscribe(params => {
      this.slug = params.get('slug')
    })
  }

  getDetailedArticle() {
    this.articleService.getDetailedArticle(this.slug).subscribe(
      article => {
        this.article = article;
      }
    )
  }

  getComments() {
    this.articleService.getArticleComments(this.slug).subscribe(
      comments => {
        this.comments = comments;
      }
    )
  }

}
