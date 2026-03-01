export class Pagination {
  private size: number;
  private lastPage: number;
  private pages: (number | null)[];

  constructor(lastPage: number, size: number = 5) {
    this.size = size;
    this.lastPage = lastPage;
    this.pages = [];
  }

  private addOverflow(left: boolean, right: boolean): void {
    if (left && this.pages[2] && this.pages[1]) {
      if (this.pages[1] !== undefined && this.pages[2] - this.pages[1] === 2) {
        this.pages.splice(1, 0, 2);
      } else {
        this.pages.splice(1, 0, null);
      }
    }

    if (right) {
      const lastIndex = this.pages.length - 1;
      if (this.lastPage - (this.pages[lastIndex] as number) === 2) {
        this.pages.push(this.lastPage - 1);
      } else {
        this.pages.push(null);
      }
    }
    if (this.pages[this.pages.length - 1] !== this.lastPage) {
      this.pages.push(this.lastPage);
    }
  }

  public getPages(currPage: number): (number | null)[] {
    this.pages = [1];

    const step = Math.floor(this.size / 2);

    if (currPage <= this.size - step) {
      if (this.lastPage < this.size) {
        for (let i = 2; i <= this.lastPage; i++) {
          this.pages.push(i);
        }
      } else {
        for (let i = 2; i < this.size; i++) {
          this.pages.push(i);
        }
        this.addOverflow(false, true);
      }
    } else if (this.lastPage <= currPage + step) {
      for (let i = this.lastPage - this.size + 2; i < this.lastPage; i++) {
        this.pages.push(i);
      }
      this.addOverflow(true, false);
    } else {
      const adjustedStep = step - 1;
      const start = currPage - adjustedStep;
      const end = currPage + adjustedStep;

      for (let i = start; i <= end; i++) {
        this.pages.push(i);
      }
      this.addOverflow(true, true);
    }

    return this.pages;
  }
}
