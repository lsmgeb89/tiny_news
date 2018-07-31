import React from 'react';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';
import Auth from '../Auth/Auth';

// NewsPanel is responsible for communication with back-end and generating NewsCard

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = { news:null };
  }

  handleScroll() {
    // get how many pixels in y axis
    // for compatibility, use three methods
    const scrollY = window.scrollY
      || window.pageYOffset
      || document.documentElement.scrollY;

    // if users scroll down to bottom
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      console.log('Loading more news!');
      this.loadMoreNews();
    }
  }

  // override
  componentDidMount() {
    this.loadMoreNews();
    // use lodash to wrap loadMoreNews with debouncing
    // trigger once in 1000ms
    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
    // bind scroll event with loadMoreNews to implement auto loading
    // use arrow function to pass this down to handleScroll
    window.addEventListener('scroll', () => this.handleScroll());
  }

  loadMoreNews() {
    const news_url = 'http://' + window.location.hostname + ':3000' + '/news';
    const request = new Request(
      news_url,
      {
        method:'GET',
        headers: {
          'Authorization': 'bearer ' + Auth.getToken()
        },
        cache:'no-cache'
      });

    fetch(request)
      .then(res => res.json())
      .then(news_list => {
        this.setState({
          news: this.state.news ? this.state.news.concat(news_list): news_list,
        });
      });
  }

  // because the number of news card to render is dynamic, we need a function to deal with it.
  renderNews() {
    // map each news to a clickable item
    const news_list = this.state.news.map( single_news => {
      return(
        // key is required by react to achieve minimal refresh in virtual dom
        // pass a single news down to NewsCard as a property
        <a className='list-group-item' key={single_news.digest} href="#">
          <NewsCard news={single_news} />
        </a>
      );
    });

    // show whole news list
    return(
      <div className="container-fluid">
        <div className="list-group">
          {news_list}
        </div>
      </div>
    );
  }

  render() {
    if (this.state.news) { // if we have news, show it
      return(
        <div>
          { this.renderNews() }
        </div>
      );
    } else { // otherwise, show loading
      return(
        <div>
          Loading ...
        </div>
      );
    }
  }
}

export default NewsPanel;
