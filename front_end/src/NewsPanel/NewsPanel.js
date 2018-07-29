import React from 'react';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';

// NewsPanel is responsible for communication with back-end and generating NewsCard

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = { news:null };
  }

  // override
  componentDidMount() {
    this.loadMoreNews();
  }

  loadMoreNews() {
    this.setState({
      // fake json news data to test front-end UI becaues currently there is no back-end
      news: [
        {
          'url': 'http://us.cnn.com/2017/02/15/politics/andrew-puzder-failed-nomination/index.html',
          'title': "Inside Andrew Puzder's failed nomination",
          'description': "In the end, Andrew Puzder had too much baggage -- both personal and professional -- to be confirmed as President Donald Trump's Cabinet.",
          'source': 'cnn',
          'urlToImage': 'http://i2.cdn.cnn.com/cnnnext/dam/assets/170215162504-puzder-trump-file-super-tease.jpg',
          'digest': '3RjuEomJo26O1syZbU7OHA==\n',
          'reason': 'Recommend'
        },
        {
          'title': 'Zero Motorcycles CTO Abe Askenazi on the future of two-wheeled EVs',
          'description': "Electric cars and buses have already begun to take over the world, but the motorcycle industry has been much slower to put out all-electric and hybrid models...",
          'url': "https://techcrunch.com/2017/03/23/zero-motorcycles-cto-abe-askenazi-on-the-future-of-two-wheeled-evs/",
          'urlToImage': "https://tctechcrunch2011.files.wordpress.com/2017/03/screen-shot-2017-03-23-at-14-04-01.png?w=764&h=400&crop=1",
          'source': 'techcrunch',
          'digest': "3RjuEomJo26O1syZbUdOHA==\n",
          'time': "Today",
          'reason': "Hot"
       }
      ]
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
