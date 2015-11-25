var CommentBox = React.createClass({displayName: 'CommentBox',
	getInitialState: function() {
		return {data: []};
	},

	loadCommentsFromServer: function() {
		$.ajax({
			url: this.props.url,
			dataType: 'json',
			cache: false,
			success: function(data) {
				this.setState({data: data});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error(this.props.url, status, err.toString());
			}.bind(this)
		});
	},

	componentDidMount: function() {
    this.loadCommentsFromServer();
    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
	
	render: function() {
		return (
			<div class="commentBox">
				<h1>Comments</h1>
				<CommentList data={this.state.data} />
			</div>
		)
	}
});

var CommentList = React.createClass({
	render: function() {
		var commentNodes = this.props.data.map(function(comment) {
			return (
				<Comment author={comment.author} key={comment.id} sent={comment.sent}>
					{comment.text}
				</Comment>
			);
		});
		return (
			<div className="commentList">
				{commentNodes}
			</div>
		)
	}
});

var Comment = React.createClass({
	rawMarkup: function() {
		var rawMarkup = marked(this.props.children.toString(), {sanitize: true});
		return { __html: rawMarkup };
	},

	render: function() {
		return (
			<div className="panel panel-default comment">
				<div className="panel-body">
					<h3 className="commentAuthor">
						{this.props.author}
					</h3>
					<span dangerouslySetInnerHTML={this.rawMarkup()} />
					{this.props.sent}
				</div>
			</div>
		);
	}
});

ReactDOM.render(
	<CommentBox url="/dashboard/comments" pollInterval={2000}/>,
	document.getElementById('comments')
);