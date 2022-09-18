using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class Notes
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "یادداشت")]
        [Required(ErrorMessage = "لطفا {0} را به درستی وارد کنید")]
        [MaxLength(500, ErrorMessage = "تعداد حروف بیشتر از حد مجاز است")]
        public string Note { get; set; }

        public virtual Users? Users { get; set; } = null;
        public virtual Posts? Posts { get; set; } = null;
    }
}
