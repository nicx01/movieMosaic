import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TinderRatingComponent } from './tinder-rating.component';

describe('TinderRatingComponent', () => {
  let component: TinderRatingComponent;
  let fixture: ComponentFixture<TinderRatingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TinderRatingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TinderRatingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
