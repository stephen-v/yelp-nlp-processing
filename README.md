# yelpdata_processing
yelp comments dataset processing

## Mysql SQL Script

1、Restaurants
```SQL
create table if not exists yelp_db.restaurants
(
	business_id varchar(50) charset utf8 not null,
	name varchar(100) null,
	categories varchar(500) charset utf8 null,
	review_count int null,
	constraint Restaurants_business_id_uindex
		unique (business_id)
)
;

alter table yelp_db.restaurants
	add primary key (business_id)
;
```
2、Reviews
``` SQL
create table if not exists yelp_db.restaurant_reviews
(
	business_id varchar(50) charset utf8 null,
	review_id varchar(50) charset utf8 null,
	text varchar(5000) charset utf8 null,
	star int null,
	constraint restaurant_reviews_review_id_uindex
		unique (review_id)
)
;

create index restaurant_reviews_business_id_index
	on yelp_db.restaurant_reviews (business_id)
;
```