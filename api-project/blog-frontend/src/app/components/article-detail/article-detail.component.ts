import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ArticleService } from 'src/app/services/article/article.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.component.html',
  styleUrls: ['./article-detail.component.css']
})
export class ArticleDetailComponent implements OnInit, OnDestroy {
  paramsSubscription: Subscription;
  articleSubscription: Subscription;
  commentSubscription: Subscription;

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

  ngOnDestroy(): void {
    this.paramsSubscription.unsubscribe();
    this.articleSubscription.unsubscribe();
    this.commentSubscription.unsubscribe();
  }

  getSlugFromParams() {
    this.paramsSubscription = this.route.paramMap.subscribe(params => {
      this.slug = params.get('slug')
    })
  }

  getDetailedArticle() {
    this.articleSubscription = this.articleService.getDetailedArticle(this.slug).subscribe(
      article => {
        this.article = article;
      }
    )
  }

  getComments() {
    this.commentSubscription = this.articleService.getArticleComments(this.slug).subscribe(
      comments => {
        this.comments = comments;
      }
    )
  }

}
